---
layout: post
title: "Crappy Code"
description: "..."
date: 2022-11-17 7:00:00 +0000
# image: assets/pics/django32-query-perf.png
---

Let me tell a little storry about the following code snippet:

```python
try:
    form_templates = FormTemplate.objects.filter(company__company_associations__tree_id=tree_id, is_public=1,
                                                    deleted=0).exclude(company_id=company_id)
    for template in form_templates:
        if int(rdbms_id) == template.id:
            load_brandhub = True
except:
    pass
```

This code was committed 6 years ago and it was used until very recently by every larger company that bought one my clients SaaS and it's terrible in many ways:

1. It's super wasteful
2. Hard to understand
3. Broken

This code was serving the customers for 6 years before it finally broke down. The company where it was written grew from 10 employees to over 120 and this code continued to work. It was serving customers big and small and it still worked, until a very large customer started using it. After that it finally broke down and got replaced with:

```python
load_brandhub = (
    FormTemplate.objects.filter(
        id=rdbms_id,
        company__company_associations__tree_id=tree_id,
        is_public=1,
        deleted=0,
    )
    .exclude(company_id=company_id)
    .exists()
)
```

The lesson is that even bad code can be good enough for a very long time. Don't worry about perfection, ship your code and fix it when it breaks[0]! 🚢

[0] Please don't use this approach when writing software where people's lives are at stake 🙏
