Run the blog locally using 

```sh
# Install ruby
brew install ruby rbenv

# rbenv install 3.3.0
rbenv global 3.3.0

# Install bundler (if you haven't)
gem install bundler


# Install dependencies
bundle install

# Run Jekyll with live reload
bundle exec jekyll serve --livereload
```