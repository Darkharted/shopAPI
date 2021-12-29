from django.http import request
import product
from model_utils import fields
from rest_framework import serializers
from .models import Product, ProductReview


class ProductListSerializer(serializers.ModelSerializer):
    """
    Класс для перевода типов данных Python в json формат
    """
    class Meta:
        """
        Класс для передачи дополнительных данных
        """
        model = Product
        exclude = ("description", "image", "created_at")
        # fields = ('id', 'title', 'price', 'status', 'description',)
        # fields = "__all__"
        # fields = ("title", "status", "description", "price", "imagen")

    

class ProductDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = "__all__"
        
        def to_representation(self, instance):
            representation = super(ProductDetailSerializer, self).to_representation(instance)
            representation['reviews'] = ProductReviewSerializer(
                ProductReview.objects.filter(product=instance.id),
                many=True
            ).data
            return representation

# class ProductUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = "__all__"


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta(ProductDetailSerializer.Meta):
        pass
        # model = Product
        # fields = "__all__"

    def validate_price(self,price):
        if price < 100:
            raise serializers.ValidationError("Цена не может быть отрицательной и меньше 100")

        return price
 
class ProductReviewSerializer(serializers.ModelSerializer):
    
    product_title = serializers.SerializerMethodField("get_product_title")

    class Meta:
        model = ProductReview
        fields = "__all__"
    
    def get_product_title(self, product_review):
        title = product_review.product.title
        return title



# class ProductDeleteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = "__all__"


class ProductReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductReview
        # fields = '__all__'
        exclude = ('author', )
    
    def validate_product(self, product):
        # ProductReview.objects.filter(product=product)
        if self.Meta.model.objects.filter(product=product).exists():
            raise serializers.ValidationError(
                "Вы уже оставляли отзыв на данный продукт"
            )
        return product
    
    def validate_rating(self, rating):
        if rating not in range(1,6):
            raise serializers.ValidationError(
                "Рейтинг должен быть от 1 до 5"
            )
        return rating

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        # print(dir(instance) ,'Hellooooooo')
        if not request.user.is_anonymous:
            representation['author'] = request.user.email
        
        return representation
        




