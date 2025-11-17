---
layout: default
title: 1 line linux distro review
---

Most developers (presumably people reading this blog) are familiar with linux on server but I doubt many folks have tried maintaining a Linux machine with maybe the exception of Ubuntu. Over the past few weeks I've spent a lot of time reviving some of my older machines, installing many different distros and tweaking them and I wanted to share my 1-line reviews in case they help someone else looking to take the plunge.

## TL;DR what does Mark use
* [Pop!_OS](https://system76.com/pop/): for my main desktop which I use both for local development of PyTorch and gaming
* [Omarchy](https://omarchy.org/): on my thinkpad T14 laptop, it's beautiful OOB and Wayland really lets me manage my 14 inch display really efficiently
* [Bazzite](https://bazzite.gg/): I've repursosed a mini Framework desktop PC as my home entertainment system and I mostly use this to play games on the couch

But back to the guide!

The key to remember is that Linux distros differ along 2 important dimensions
1. The core audience which determines which software gets installed OOB
2. The release and backwards compatibility strategy

Your preferences with 1 and comfort level with 2 is primarily what'll determine your choices.

## The reviews

* [Ubuntu](https://ubuntu.com/): This is what almost everyone uses and for good reason, it's stable, it rarely breaks and it has a OS X like aesthetic with Gnome. It's a great choice but at least for AI developers I now recommend [Pop!_OS](https://system76.com/pop/) instead which is Ubuntu based but also ships well tested NVIDIA drivers so you don't have to muck around yourself installing them (something people spend way too much time on vanilla ). 
* [Red Hat]( https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux): Is an entreprise Linux distro which requires buying a license so similar distros that have popped up that are community supported are [Fedora](https://www.fedoraproject.org/) and [CentOS](https://www.centos.org/). These are all reasonable choices if you're running linux on server where reliability and security are the most important considerations. At least for Desktop though this is not as big of a deal
* [Mint](https://linuxmint.com/): If you're coming from Windows this is a reasonable first choice using the defaults from KDE but I wouldn't personally use it anymore
* [Omarchy](https://omarchy.org/): Omarchy is a fairly opiniated arch based distro, I like it a lot because it can show you directionally how you could set something up with beautiful themes and tons of clever keyboard shortcuts and of course the wonderful Wayland tiling manager. I don't know if I'll use Omarchy for a long time but using it for a few weeks confirmed to me that I never want to use Windows or Mac ever again 
* [Arch](https://archlinux.org/): Both Arch and [Nix](https://nixos.org/) have often been described to me as the dark souls of linux distros, the main challenge with Arch is it does rolling releases so everytime you update your packages you're basically installing untested nightlies of everything which means almost everything is expected to break. With things like Nix you can rollback towards something that did work easily but still, this is a type of distro I expect to do hobby projects on but not something I expect to main anytime soon
* [Raspberry Pi OS](https://kodi.tv/download/raspberry-pi/): Doesn't really need to be its own thing but it has reasonable defaults like it works well on ARM, it recognizes the pins on the physical hardware and it comes with a bunch of preinstalled software for students
* [Bazzite](https://bazzite.gg/): Bazzite is basically primarily a gaming console sort of distro, I've repurposed an old PC of mine and hooked it up to my TV, it comes preinstalled with all sorts of bluetooth drivers for various wireless controllers, there's no login because again you would expect to start playing all your steam and PC games. Another similar distro would be [Steam OS](https://store.steampowered.com/steamos) by Valve which has really helped make Linux gaming a reality and most notably supported [protondb](https://www.protondb.com/) which will run Windows games on Linux without emulation but translating Windows specific syscalls using [Wine](https://www.winehq.org/)
* [Kali](https://www.kali.org/): Something I used when I was much younger but it was fun to learn basics of security, again a lot of linux distros are primarily about focusing on a specific audience with tools for that audience, no OS makes this clearer than Kali

## Outro

If you dont know how to configure something, its almost certainly the case that Claude or Codex know how. 

Finally I do want to give a special shoutout to [Tailscale](https://tailscale.com/), managing tons of machines at home can be clunky if you're lugging around a mouse, keyboard and monitor per device. What tailscale lets you do is after 2 commands you can easily ssh into your machines, configure them and set them up in you case you run into a rare issue. Another fancier choice would be [JetKVM](https://jetkvm.com/) where you plug in a little dongle into your computer, you get an IP on the display and then you can remote desktop with full GUI support using your browser.

Overall it's been quite remarkable to me how good these distros and how strong the support has been despite them being mostly volunteer maintained projects. If we zoom out in the distant future, it's fairly obvious to me that Linux will be the main choice of developers, AI researchers and gamers so please try any of the above distros out, I promise you'll be pleasantly surprised.
