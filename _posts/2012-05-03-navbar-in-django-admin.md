---
layout: post
title: "Navbar in Django Admin"
category: 
tags: [django, python, coding]
---
{% include JB/setup %}

I wanted to add navigation to the Django top bar. The idea was that all of the installed apps should show up in the navbar beside the brand name. This is a screenshot of the working solution in action:

<a href="/assets/pics/django-menu.png" style="text-align:center;"><img class="" src="/assets/pics/django-menu.png"  width="700" alt="django menu" /></a>

A solution
----------

I hacked together a solution using a custom context processor in order to feed the installed applications to every template in the django admin site. I borrowed most of the code from the admin index view. `context_processors.py`:

{% highlight python %} 
    from django.utils.text import capfirst
    from django.db.models import get_models
    from django.utils.safestring import mark_safe
    from django.contrib.admin import ModelAdmin
    from django.contrib.admin.validation import validate

    # get_models returns all the models, but there are 
    # some which we would like to ignore
    IGNORE_MODELS = (
        "sites",
        "sessions",
        "admin",
        "contenttypes",
    )

    def app_list(request):
        '''
        Get all models and add them to the context apps variable.
        '''
        user = request.user
        app_dict = {}
        admin_class = ModelAdmin
        for model in get_models():
            validate(admin_class, model)
            model_admin = admin_class(model, None)
            app_label = model._meta.app_label
            if app_label in IGNORE_MODELS:
                continue
            has_module_perms = user.has_module_perms(app_label)
            if has_module_perms:
                perms = model_admin.get_model_perms(request)
                # Check whether user has any perm for this module.
                # If so, add the module to the model_list.
                if True in perms.values():
                    model_dict = {
                        'name': capfirst(model._meta.verbose_name_plural),
                        'admin_url': mark_safe('%s/%s/' % (app_label, model.__name__.lower())),
                    }
                    if app_label in app_dict:
                        app_dict[app_label]['models'].append(model_dict)
                    else:
                        app_dict[app_label] = {
                            'name': app_label.title(),
                            'app_url': app_label + '/',
                            'has_module_perms': has_module_perms,
                            'models': [model_dict],
                        }
        app_list = app_dict.values()
        app_list.sort(key=lambda x: x['name'])
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])
        return {'apps': app_list}
{% endhighlight python %}

        
We add the custom context processor to the `settings.py`:
 
{% highlight python %} 
    TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.contrib.messages.context_processors.messages",
        "context_processors.app_list"
    )
{% endhighlight python %}

With the context processor in place we should have an 'apps' variable available in our admin templates. The only thing left to do is to add the code that renders the installed applications. I am using [twitter bootstrap](http://twitter.github.com/bootstrap) for the navbar. Here is my `templates/admin/base.html`: 

{% highlight html %}
    <ul class="nav">
        { % for app in apps % }

        <li class="dropdown">
        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
            { % trans app.name % }<b class="caret"></b>
        </a>

        <ul class="dropdown-menu">
            { % for model in app.models % }
            <li><a href="/{ { model.admin_url } }">{ { model.name } }</a></li>
            { % endfor % }
        </ul>
        </li>
        { % endfor % } 
    </ul>
{% endhighlight html %}

**Note:** I had to add spaces to the { % and { { tags as jekyll/markdown doesn't seem to be able to handle them in code segments.

This is pretty much it. Suggestions for improvements are welcome!

