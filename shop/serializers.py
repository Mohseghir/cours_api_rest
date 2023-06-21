from rest_framework.serializers import ModelSerializer, SerializerMethodField, \
    CharField, ValidationError

from shop.models import Category, Product, Article


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'date_created', 'date_updated', 'name', 'price', 'product']

        # Le prix doit être supérieur à 1 €.
        def validate_price(self, value):
            if value < 1:
                raise ValidationError('Price must be greater than 1')
            return value

        # Le produit associé doit être actif.
        def validate_product(self, value):
            if value.active is False:
                raise ValidationError('Inactive product')
            return value


class CategoryListSerializer(ModelSerializer):
    name = CharField()  # Ajoutez cette ligne pour inclure le champ 'name

    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name', 'description']

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise ValidationError('Category already exists')
        return value

    def validate(self, data):
        # Effectuons le contrôle sur la présence du nom dans la description
        if data['name'] not in data['description']:
            # Levons une ValidationError si ça n'est pas le cas
            raise ValidationError('Name must be in description')
        return data


class CategoryDetailSerializer(ModelSerializer):
    products = SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name', 'products']

    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductListSerializer(queryset, many=True)
        return serializer.data


class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'category']


class ProductDetailSerializer(ModelSerializer):
    articles = SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'category', 'articles']

    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data
