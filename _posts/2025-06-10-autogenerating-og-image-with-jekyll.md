---
layout: post
title: Autogenerating og:images with Jekyll
date: 2025-06-10 02:38 +0100
---

This blog has been a static site powered by [Jekyll](https://jekyllrb.com/) for [over 13 years](https://blog.pecar.me/why-i-chose-jekyll), and I've been happy with the setup. After all this time, I still enjoy using my code editor to write new posts and `git commit` and `git push` to publish them.

However, there was one issue that often discouraged me from writing: I had to switch out of the code editor to generate the Open Graph image that appears on social media when I share the link to the blog post. For this particular blog post, this image looks like this:

![og image for this post](assets/images/og/posts/autogenerating-og-image-with-jekyll.png)

## jekyll-og-image

Today, I finally set aside some time to figure out how to automate this process. Luckily, there exists a Jekyll plugin that solves this problem: [jekyll-og-image](https://github.com/igor-alexandrov/jekyll-og-image).

Before I could use jekyll-og-image, I had to first configure [jekyll-seo-tag](https://github.com/jekyll/jekyll-seo-tag). At first, I was annoyed by this, but in the end, I was delighted with the result. After adding a few settings into `_config.yml`, the plugin allowed me to remove over 20 lines of tags from my layout:

```patch
{% raw %}
diff --git a/_layouts/default.html b/_layouts/default.html
index abb2143a..362c5e4 100644
--- a/_layouts/default.html
+++ b/_layouts/default.html
@@ -11,32 +11,9 @@
 <meta name="viewport" content="width=device-width, initial-scale=1" />
 <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
 <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
-  <!-- Primary Meta Tags -->
-  <title>{{ page.title }}</title>
-  <meta name="title" content="{{ page.title }}">
-  <meta name="description" content="{{ page.description }}" />
-  <meta name="author" content="{{ site.author.name }}" />
-  <link rel="canonical" href="{{site.url }}{{ page.url }}" />
-
-  <!-- Open Graph / Facebook -->
-  <meta property="og:type" content="website">
-  <meta property="og:url" content="{{site.url }}{{ page.url }}" />
-  <meta property="og:title" content="{{ page.title }}" />
-  <meta property="og:description" content="{{ page.description }}" />
-  {% if page.image %}
-  <meta property="og:image" content="{{site.url }}/{{ page.image }}" />
-  {% else %}
-  <meta property="og:image" content="{{site.url }}/assets/me.jpg" />
-  {% endif %}
-  <!-- Twitter -->
-  <meta name="twitter:card" content="summary_large_image" />
-  <meta name="twitter:creator" content="@anze3db" />
-  <meta name="twitter:title" content="{{ page.title }}" />
-  {% if page.image %}
-  <meta name="twitter:image" content="{{site.url }}/{{ page.image }}" />
-  {% else %}
-  <meta name="twitter:card" content="summary" />
-  {% endif %}
+  {% seo %}
+
 <!-- RSS Link -->
 <link rel="alternate" type="application/rss+xml" href="{{ production_url }}/feed.xml" title="{{ site.title }}" />
 <!-- CSS -->
{% endraw %}
```

👏

Once jekyll-seo-tag was configured, I had to install one more dependency: [libvips](https://www.libvips.org/). jekyll-og-image uses this image processing library to generate the images. I installed it with Brew but I also needed to add it to my GitHub Actions runner as documented by the [jekyll-og-image docs](https://github.com/igor-alexandrov/jekyll-og-image?tab=readme-ov-file#installation).

After that, I was finally able to add the `gem 'jekyll-og-image'` to my `Gemfile` and start generating the images as part of the `Jekyll build` command. But of course the first build failed! 💥

## Invalid markup in text

The build failed with the following stack trace:

```
/opt/homebrew/lib/ruby/gems/3.3.0/gems/ruby-vips-2.2.4/lib/vips/operation.rb:228:in `build': text: invalid markup in text (Vips::Error)
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/ruby-vips-2.2.4/lib/vips/operation.rb:481:in `call'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/ruby-vips-2.2.4/lib/vips/image.rb:234:in `method_missing'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-og-image-2.0.0/lib/jekyll_og_image/element/text.rb:25:in `apply_to'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-og-image-2.0.0/lib/jekyll_og_image/element/canvas.rb:30:in `text'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-og-image-2.0.0/lib/jekyll_og_image/generator.rb:123:in `add_header'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-og-image-2.0.0/lib/jekyll_og_image/generator.rb:85:in `generate_image_for_document'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-og-image-2.0.0/lib/jekyll_og_image/generator.rb:47:in `block in process_collection'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-og-image-2.0.0/lib/jekyll_og_image/generator.rb:26:in `each'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-og-image-2.0.0/lib/jekyll_og_image/generator.rb:26:in `process_collection'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-og-image-2.0.0/lib/jekyll_og_image/generator.rb:10:in `block in generate'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-og-image-2.0.0/lib/jekyll_og_image/generator.rb:9:in `each'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-og-image-2.0.0/lib/jekyll_og_image/generator.rb:9:in `generate'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-4.3.4/lib/jekyll/site.rb:193:in `block in generate'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-4.3.4/lib/jekyll/site.rb:191:in `each'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-4.3.4/lib/jekyll/site.rb:191:in `generate'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-4.3.4/lib/jekyll/site.rb:79:in `process'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-4.3.4/lib/jekyll/command.rb:28:in `process_site'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-4.3.4/lib/jekyll/commands/build.rb:65:in `build'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-4.3.4/lib/jekyll/commands/build.rb:36:in `process'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-4.3.4/lib/jekyll/command.rb:91:in `block in process_with_graceful_fail'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-4.3.4/lib/jekyll/command.rb:91:in `each'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-4.3.4/lib/jekyll/command.rb:91:in `process_with_graceful_fail'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-4.3.4/lib/jekyll/commands/build.rb:18:in `block (2 levels) in init_with_program'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/mercenary-0.4.0/lib/mercenary/command.rb:221:in `block in execute'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/mercenary-0.4.0/lib/mercenary/command.rb:221:in `each'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/mercenary-0.4.0/lib/mercenary/command.rb:221:in `execute'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/mercenary-0.4.0/lib/mercenary/program.rb:44:in `go'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/mercenary-0.4.0/lib/mercenary.rb:21:in `program'
 from /opt/homebrew/lib/ruby/gems/3.3.0/gems/jekyll-4.3.4/exe/jekyll:15:in `<top (required)>'
 from /opt/homebrew/lib/ruby/gems/3.3.0/bin/jekyll:25:in `load'
 from /opt/homebrew/lib/ruby/gems/3.3.0/bin/jekyll:25:in `<top (required)>'
 from /opt/homebrew/Cellar/ruby/3.3.5/lib/ruby/3.3.0/bundler/cli/exec.rb:58:in `load'
 from /opt/homebrew/Cellar/ruby/3.3.5/lib/ruby/3.3.0/bundler/cli/exec.rb:58:in `kernel_load'
 from /opt/homebrew/Cellar/ruby/3.3.5/lib/ruby/3.3.0/bundler/cli/exec.rb:23:in `run'
 from /opt/homebrew/Cellar/ruby/3.3.5/lib/ruby/3.3.0/bundler/cli.rb:455:in `exec'
 from /opt/homebrew/Cellar/ruby/3.3.5/lib/ruby/3.3.0/bundler/vendor/thor/lib/thor/command.rb:28:in `run'
 from /opt/homebrew/Cellar/ruby/3.3.5/lib/ruby/3.3.0/bundler/vendor/thor/lib/thor/invocation.rb:127:in `invoke_command'
 from /opt/homebrew/Cellar/ruby/3.3.5/lib/ruby/3.3.0/bundler/vendor/thor/lib/thor.rb:527:in `dispatch'
 from /opt/homebrew/Cellar/ruby/3.3.5/lib/ruby/3.3.0/bundler/cli.rb:35:in `dispatch'
 from /opt/homebrew/Cellar/ruby/3.3.5/lib/ruby/3.3.0/bundler/vendor/thor/lib/thor/base.rb:584:in `start'
 from /opt/homebrew/Cellar/ruby/3.3.5/lib/ruby/3.3.0/bundler/cli.rb:29:in `start'
 from /opt/homebrew/Cellar/ruby/3.3.5/lib/ruby/gems/3.3.0/gems/bundler-2.5.18/exe/bundle:28:in `block in <top (required)>'
 from /opt/homebrew/Cellar/ruby/3.3.5/lib/ruby/3.3.0/bundler/friendly_errors.rb:117:in `with_friendly_errors'
 from /opt/homebrew/Cellar/ruby/3.3.5/lib/ruby/gems/3.3.0/gems/bundler-2.5.18/exe/bundle:20:in `<top (required)>'
 from /opt/homebrew/opt/ruby/bin/bundle:25:in `load'
 from /opt/homebrew/opt/ruby/bin/bundle:25:in `<main>'
```

After a small amount of frustration I figured out that half of the images were generated correctly. This made me think that the root cause had to be one particular blog post. Enabling `verbose` mode led me to a blog post that had an `&` symbol in the title. There is [a closed issue about this](https://github.com/igor-alexandrov/jekyll-og-image/issues/1), but it looks like it either regressed or wasn't fixed fully. My solution was simple: I replaced the ampersand with an `and` & moved on with my life!

## Second problem

I thought I was out of the woods at this point but after I pushed the changes to production the generated images were returning 404s. I verified that the images were being generated correctly in the GitHub action and then finally found out that they were not copied to the `_site` folder correctly. The `_site` includes all the static files that get uploaded to GitHub Pages so if files are missing they won't be accessible once the site is deployed. There is also an [existing issue about this as well](https://github.com/igor-alexandrov/jekyll-og-image/issues/14).

I noticed that rebuilding the project a second time correctly copies the generated images to the `_site` folder, so my solution was to run the build twice:

```yaml
      - name: Build with Jekyll
        # Outputs to the './_site' directory by default
        # Build twice because the first run doesn't copy generated images
        run: |
          bundle exec jekyll build --baseurl "${{ steps.pages.outputs.base_path }}"
          bundle exec jekyll build --baseurl "${{ steps.pages.outputs.base_path }}" 
```

## Fin

And that was it. I now have og:images auto-generated by Jekyll! Hopefully, this will remove some of the friction and encourage me to blog more often! 🤞
