---
title: A tour of torchdata
layout: default
---

# A batch's journey: torchdata internals

The core code is in `torchdata`. About 3237 lines dedicated to datapipes and about 376 lines deddicated towards dataloaderv2 but the repo is moving fast and this document may be out of date in a few weeks with regards to specifics but not core ideas.

`torchdata` is fundamentally well about loading data into `PyTorch` with the familiar iterator pattern we all know and love

```python
for batch in dataloader:
  model.forward(batch)
```

But when you're loading in a batch you're already assuming that it's nice and clean in a tensor format but more practically it's going to be some raw image or text datat or increasingly more something multimodal. You're going to read the data, decode it, split it into train and test, shuffle each partition then pass it to different workers and that whole sequence of operations can be represented as a **graph** which in `torchdata` terminology is called a `datapipe`. It's called datapipe because you can imagine a batch *piping* through it - yeah naming things is hard.


Typically as an ML practicioner you'd focus more on your `nn.Module` but as GPUs are getting faster the bottleneck is no longer how quickly you can do matrix multiplication but how quickly you can feed data to a GPU a metric called `memory bandwidth`. Any improvements in the performance of data loading directly translates into improvements in memory bandwidth. So what is torchdata and how does it help increase memory bandwidth?

> torchdata is a library to create dataloaders from datapipes (with lots of useful modular abstractions)

The rest of this doc is really about understanding those *useful modular abstractions*, why they're interesting and how they were designed.

# What's a datapipe?


`torchdata/datapipes` splits into two main folders `iter` and `map` for iterative and map style datasets respectively. Iterative datasets means you are not allowed random access and is the newer model wheras map style datasets is what traditionally people have been doing with torchdata. An `iter` dataset is one wherey you can only access the next element wheras a `map` dataset is one where you can index into any element. So `map` style datasets are more expressive and can be used to implement an `iter` style dataset and that's exactly what has been done historically. However, because `iter` style datasets are more restrictive we can actually make them more performant with more clever prefetching logic and caching.

## map style datapipes

All the interesting code is in `map/util/` which includes a cacheholder, converter and unzipper

An unzipper allows you to to turn a single node in a graph with a tuple into several nodes and general trend you'll find in `torchdata` is its about defining a datapipe graph using operations that should be familiar to you as a python programmer especially if you've ever used something like `functools`.

```python
>>> source_dp = SequenceWrapper([(i, i + 10, i + 20) for i in range(3)])
>>> dp1, dp2, dp3 = source_dp.unzip(sequence_length=3)
>>> list(dp1)
[0, 1, 2]
>>> list(dp2)
[10, 11, 12]
>>> list(dp3)
[20, 21, 22]
```

To make it easier for users to move from traditional map style datasets already available in open source to iterable style datasets they can use `MapToIterConverterIterDataPipe` which is actually fairly straightforward because you pretend the map style dataset is iterable.

```python
def __iter__(self):
for idx in self.indices:
    yield self.datapipe[idx]
```

In memory cache simply uses a python dictionary but over time it makes more sense to use more resilient forms of caching by integrating with external services or libraries like `redis`.

```python
def __getitem__(self, index) -> T_co:
    if index not in self.cache:
        self.cache[index] = self.source_dp[index]  # type: ignore[index]
    return self.cache[index]  
```

## iterable datasets

### load

In `iter/load/` you'll see lots of examples of using remote object stores. Regardless of whether you're using `fsspec`, `aistore` `s3`, `http` `huggingface datasets` when implementing your own loader you need to make sure that you're returning an iterator from those services. As datasets get larger we can no longer expect that users will have them downloaded locally or that those datasets would fit in RAM so having support for remote datasets with competitive performance to local performance is becoming a must. This is another motivator for iterable style datasets because of something is if you have a large dataset and you randomly index into it you can't take advantage of data locality. Data locality is a big deal on GPUs can be responsible for an easy 10x end to end training time degredation if done really poorly.

But I digress, let's take a look at a specific remote object store wich streams in data from an HTTP endpoint. The data is streamed via a single process but eventually we can move towards reading this in a multithreaded manner.


```python
@functional_datapipe("read_from_http")
class HTTPReaderIterDataPipe(IterDataPipe[Tuple[str, StreamWrapper]]):
```

And you may have already noticed 2 strange l ooking syntax: `@functional_datapipe` and `StreamWrapper`

Unfortunately neither of those two are implemented in `pytorch/data` but are instead still in the process of being moved over from `pytorch/pytorch`


`functional_datapipe` is in `torch.utils.data.datapipes._decorator`

`@functional_datapipe` has a lot of code to make sure it's only working over a datapipe but if we remove it then what's left is simple, it registers a function on the class with a specific name

```python
class functional_datapipe(object):
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def __call__(self, cls):
        if issubclass(cls, IterDataPipe):
            IterDataPipe.register_datapipe_as_function(self.name, cls)
        elif issubclass(cls, MapDataPipe):
            MapDataPipe.register_datapipe_as_function(self.name, cls)
        return cls
```

Ok so now what is this `IterDataPipe` or `MapDataPipe` about?

`IterDataPipe` defined in `torch/utils/data/dataset.py` where as expected you need to define a function `__iter__` to use it as a dataloader

```python

    def __iter__(self) -> Iterator[T_co]:
        raise NotImplementedError

```

`T_co` is an important type that shows up a lot in `torchdata` and it stands for *Type is COvariant* which is a more general form of the Liskov Substitution principle which means that you can substitute a derived class for the base class in a function and things should work (This is the Liskov Substituion principle) but also do the reverse substitute the derived class by the base class and things should work.


The signature for `class IterableDataset(Dataset[T_co], metaclass=_DataPipeMeta):` includes a `Dataset` which has the signature ` def register_datapipe_as_function(cls, function_name, cls_to_register):` function we've been looking for that explains how the `@functional_datapipe` decorator works. Via one more layer of indirection you can see the below class method which registers a function on the class

```python
@classmethod
def register_function(cls, function_name, function):
    cls.functions[function_name] = function
```

In Python this is called monkey patching since we can dynamically allocate methods to an object at runtime and then call a datapipe as a function with a shorter name. This is convenient because by default all datapipes compose with each other, datapipes you develop will compose with datapipes that were created by the core torchdata team, your colleagues and also anyone on the internet.

For reference IterDataPipe, IterableDataSet and DataSet, MapDataPipe are interchangable because in `datapipes/__init__.py` they are overriden


TODO: `StreamWrapper` in `torch.utils.data.datapipes.utils.common` (Actually haven't found it yet)



### transform

There is support for a batch mapper which applies an operation over a batch of elements, which is useful for any sort of data preprocessing

```python
>>> from torchdata.datapipes.iter import IterableWrapper
>>> def fn(batch):
>>>     return [d + 1 for d in batch]
>>> source_dp = IterableWrapper(list(range(5)))
>>> mapped_dp = source_dp.map_batches(fn, batch_size=3)
>>> list(mapped_dp)
[1, 2, 3, 4, 5]
```

There's another variant of this function which does the same thing but then also flattens the input. In general if you've used a functional programming language then you should recognize the `map` and `flatmap` operations here

### util

This is the largest folder in the whole project and includes utilities to read compressed files like `.bz2` or `xz`, `tfrecord`, `json`, `rar`, `tar`, `webdataset` `.zip`. Some of these are aggregated into the more generic `decompressor.py`

Utilities to zip multiple datapipes into one or unzip a single datapipe into multiple ones.

Utilities to multiplex from multiple datapipes so read one from each datapipe until are exhausted, useful for multiprocessing usecases

Cycle allows you to never exhaust a datapipe, useful for multi epoch training where you're iterating over a dataset more than once.

```python
    def __iter__(self) -> Iterator[T_co]:
        i = 0
        while self.count is None or i < self.count:
            yield from self.source_datapipe
            i += 1
```

I like to think of `torchdata` as having introduced its own data preprocessing algebra. Something I haven't answered to myself is why did we need to create our own, why not instead leverage existing primitives that were created by python or functools. I believe the answer to this is because doesn't provide an easy way to multiple dispatch core features and this would be easier in other languages like Julia.


## Create a datapipe graph
At a high level torchdata is a library to create a data processing graph, we've already show how it has a bunch of nodes that do useful things like batching or shuffling but then also it has utilities to setup a DAG of operations by multiplexing, splitting or merging nodes together.

`torchdata` tries really hard to make it so graphs are serializable, what that means is you can write the object to disk as a file and read it back, this is useful for creating checkpoints, sharing datapipes across multiple processes (python uses pickled objects to pass data between processes)

```python
def serialize_datapipe(datapipe: IterDataPipe) -> bytes:
    try:
        return pickle.dumps(datapipe)
```

Once we start talking more about Dataloaders you'll see that most of them also implement a  `__reduce_ex__` function which is defines how an object should be pickled `def __reduce_ex__(self, *args, **kwargs):`

But this idea is very powerful if you've recently played around with something like `torch.fx` where once you have a graph, you can then execute some compiler passes on it to change its behavior. So in `fx` these are called passes but in `torchdata` these are called `Adapter` and an Adapter is a class that given a `datapipe` returns a `datapipe`

```python
class Adapter:
    @abstractmethod
    def __call__(self, datapipe: DataPipe) -> DataPipe:
        pass
```

In particular we can do clever things like adding a per node timeout without having to change the graph. What's interesting about this there are two important utils functions `torch.utils.data.graph.traverse` which given a datapipe will return the corresponding graph and given a graph you can get all the individual datapipes by using `torch.utils.data.graph_settings.get_all_graph_pipes(graph)`

```python
class CacheTimeout(Adapter):
    def __call__(self, datapipe: DataPipe) -> DataPipe:
        graph = torch.utils.data.graph.traverse(datapipe, only_datapipe=True)
        all_pipes = torch.utils.data.graph_settings.get_all_graph_pipes(graph)
        cache_locks = {pipe for pipe in all_pipes if isinstance(pipe, _WaitPendingCacheItemIterDataPipe)}

        for cache_lock in cache_locks:
            cache_lock.set_timeout(self.timeout)

        return datapipe
```

Conceptually this idea is very similar to how `torch.fx` does graph transformations and in `dataloader2/graph.py` this becomes even more explicit with functions that allow you to remove an individual datapipe from a graph, replace or add one. Effectively we can do graph surgery and this is powerful because let's say you want to build a memory profiler per datapipe well that's an Adapter or maybe you want take a graph and set some reasonable defaults on nodes that can also be an Adapter.

Datapipes in general need to be serializable so this also means you can change datapipes during training to change their functionality without restarting your program let's say to add more debugging functionality and then you can revert it back after you found the bug.

Some work that doesns't exist yet is we could enhance each datapipe in a graph to have some runtime information associated with it, as in run this datapipe with these 2 CPU cores or run this datapipe with a GPU or run this node of a datapipe with 2 processes and 8 threads. But this is possible again because of the graph surgery we wouldn't need to change the way we define a graph but would define a `class RunTime(Adapter)` to make this happen. We can replace that do image decoding with accelerated versions of them without forcing users to introduce any specific optimizations to their code or workflows.

Once I grokked this `Adapter` pattern, I got a lot more excited about the potential of `torchdata`.




## Why do we need a dataloader v2

So far we've been talking about datapipes which have just started to exist recently but dataloaders have existed in PyTorch for many years so why do we need to reinvent them now?

If you look at the signature, a data loader takes in 

```python
class DataLoader2(Generic[T_co]):
    def __init__(
        self,
        datapipe: IterDataPipe,
        datapipe_adapter_fn: Optional[Callable[[IterDataPipe], IterDataPipe]] = None,
        reading_service: Optional[ReadingServiceInterface] = None,
    ) -> None:
```

A dataloader can be used as a context manager because of the `__enter__` and `__exit__` dunder functions. It also has a `__next__` and `__iter__` so it can be used an iterator


`self.datapipe = self.reading_service.initialize(self.datapipe)` and then we create an iterator on the datapipe `self._datapipe_iter = iter(self.datapipe)`

Conveniently we've already covered adapters and datapipes and `DataLoader2` will only work with `IterDataPipe` so it doesn't break backwards compatibility but won't bring the same support to `MapDataPipe` or the legacy `Dataset` class unless they're explicitly converted with our helper functions.


So what is this reading service thing about?



## What is a reading service

```python
class ReadingServiceInterface(ABC):
    @abstractmethod
    def initialize(self, datapipe: IterDataPipe) -> IterDataPipe:
        """
        ReadingService traverses datapipe graph, finds executable part,
        adapts into its own datapipe, and replaces in datapipe graph.
```

The definition is not the greatest but it returns an adapted datapipe. A more concrete example would be the `MultiProcessingReadingService`

which seperates a graph by pieces and reconnects it using queues. So the same kind of graph surgery mechanisms is also used to connect multiple datapipes each working in a seperate process.

For example in the case of `MultiProcessingReadingService`
1. `initialize` a datapipe to find information about sharding, create queues, spawn processes
2. `finalize` cleanup function called to invalidate state and shutdown persistent workers 
3. for every iteration calls at beginning and end `initialize_iteration` and `finalize_iteration`

```python
class CheckpointableReadingServiceInterface(ReadingServiceInterface):
    @abstractmethod
    def checkpoint(self) -> bytes:
        pass
    @abstractmethod
    def restore(self, datapipe: IterDataPipe, serialized_state: bytes) -> IterDataPipe:
        pass
```

The MultiProcessingReadingService in addition takes in the below arguments but none of them are used yet.

```python
class MultiProcessingReadingService(ReadingServiceInterface):
    num_workers: int
    pin_memory: bool
    timeout: float
    worker_init_fn: Optional[Callable[[int], None]]
    prefetch_factor: int
    persistent_workers: bool
```    

`num_workers` set to number of cores as a rule of thumb
`pin_memory` speeds up transfer of samples from CPU to GPU. Why not set it to `true` by default
`worker_init_fn` to decide which batches get allocated to which worker
`prefetch_factor` how many elements do you prefetch beforehand, need to profile your model for OOM to figure this out
`persistent_workers` probably a good idea to set this to `true` otherwise you will have to create new workers at every iteration

`MultiProcessingReadingService` is currently being replaced by `PrototypeMultiProcessingReadingService` which in its `initialize` function will spawn or fork multiple processes and have them communicate via a Queue

```python
for worker_id in range(self.num_workers):
    ...
    self.processes.append((process, req_queue, res_queue))  # These queues are independent
    local_datapipe = communication.iter.QueueWrapper(
        communication.protocol.IterDataPipeQueueProtocolClient(req_queue, res_queue)
    )
    ...
```

The communication and queues are all defined in their own `dataloader2/communication/` where in `queue.py` a queue is nothing but a python list popped in FIFO manner and also a threading queue which locks the queue before an element is inserted or dequeued. Over time in the same now that torchdata supports multiple object stores, it could also support multiple forms of caching. Local caches are always fastest assuming no cache miss. The problem with a local python dict as a cache though is that you need to copy them per process because you can't share them which then forces you to have relatively small caches. So a different tradeoff is to use a distributed KV store like `redis` where you can cache elements and share them across a large number of workers which will help reduce the number of cache misses but sacrifice latency.

```python
class ThreadingQueue:
    def __init__(self, name="unnamed"):
        self.lock = threading.Lock()
        self.items = []
        self.name = name
```

The possible messages that a queue can get are defined in `messages.py` which overtime should probably become a protobuf format instead.

In `eventloop.py` you can see how a new worker is created by
1. Taking an existing datapipe and pickling it `new_datapipe = pickle.loads(pickle.dumps(datapipe))`
2. Loading a datapipe into a new python variable
3. Create a new request and response threading queue `req_queue = communication.queue.ThreadingQueue()`
4. Create a new process `process = threading.Thread(target=DataPipeToQueuesLoop, args=(new_datapipe, req_queue, res_queue), daemon=True)`

`protocol.py` takes care of handling messages defined in `messages.py` into the request queue and returning responses from the responses queue.


## Misc fun stuff

It's relatively easy for users to do wrong things by using `torchdata` for example it's best to shuffle before a sharding operation instead of sharding before a shuffle and so instead of asking users not to do that in documentation there is a `dataloderv2/linter.py` that can help detect these common issues for users and give out warnings instead. Over time as we learn more about best practices in using datapipes we will expand the number of warnings we give out to users since documentation just runss the risk of being stale.

In general `torchdata` abstracts away a lot of stuff so one important abstraction in streaming mode is shuffling behavior which is surprisingly tricky to get right in the iterable scenario so the teaming is creating generic interfaces to explore different shufflign behavior in `dataloader2/shuffle_spec.py`

```python
class ShuffleSpec(abc.ABC):
    """Defines a shuffle specification."""
```


## Csrc
There is a `csrc` folder which includes C bindings that are specific to the Amazon S3 plugin which is a remote object store you can interact with as if it was a local store. The plugin was authored in C++ for performance and so we turn it into a datapipe by leveraging `pybind11`

```c
PYBIND11_MODULE(_torchdata, m) {
  py::class_<S3Handler>(m, "S3Handler")
      .def(py::init<const long, const std::string&>())
```

The way to read this is we are creating a python module called `_torchdata` which has a class called `S3Handler` which has a function `__init__(param_1 : float64, param_2 : str)`


## Closing thoughts

`torchdata` is powerful because it modularizes and abstracts many important aspects of the data loading problem. You can define a DAG of data processing operations in an interface as powerful as `functools` where the nodes in the DAG can do all sorts of useful things ranging from reading from remote object stores to decoding data to shuffling. As the team continues to work on the new `dataloaderv2` they're leveraging the same abstractions to create reading services which are functions that operate over datapipes that can be used to perform powerful graph surgery to implement features like distributed data loading while using the same core functional abstractions in `torchdata`. Hopefully this document gets you excited about contributing to `torchdata`, writing it had that effect on me.


Thank you to Erjia and Kevin for correcting some misconceptions I had in this doc.
