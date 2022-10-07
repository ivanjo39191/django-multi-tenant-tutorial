from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from products.models import Product, ProductCategory

# The name of your index
product = Index('products')
# See Elasticsearch Indices API reference for available settings
product.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@registry.register_document
class ProductDocument(Document):
    category = fields.ObjectField(properties={
        'name': fields.TextField(),
        'name_en': fields.TextField(),
        'description': fields.TextField(),
        'description_en': fields.TextField(),
        'created': fields.DateField(),
        'modified': fields.DateField(),
        'image': fields.FileField(),
    })

    class Django:
        model = Product
        # we removed the type field from here
        fields = [
            'name',
            'description',
            'price',
            'created',
            'modified',
        ]

    class Index:
        name = "product"
        
@registry.register_document
class ProductCategoryDocument(Document):

    class Django:
        model = ProductCategory
        fields = [
            'name',
            'name_en',
            'description',
            'description_en',
            'created',
            'modified',
            'image'
        ]

    class Index:
        name = "productcategory"