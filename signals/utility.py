from django.utils.text import slugify


def create_slug(sender, instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    query = sender.objects.filter(slug=slug)
    exists = query.exists()
    if exists:
        new_slug = '%s-%s' %(slug, instance.id)
        return new_slug
    return slug