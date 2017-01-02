from django.utils.text import slugify


def create_slug(sender, instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = sender.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        new_slug = '%s-%s' %(slug, qs.count())
        return create_slug(sender, instance, new_slug=new_slug)
    return slug
