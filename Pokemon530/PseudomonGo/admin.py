from pyexpat import model
from django.contrib import admin
from .models import Profile
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
from .models import Player, EntityClass, Entity, Animal, AnimalImage, \
    StatusCondition, Move, Item, PlayerInventory, Rental
# Register your models here.


admin.site.register(Player)
admin.site.register(EntityClass)
admin.site.register(Entity)
admin.site.register(Animal)
admin.site.register(AnimalImage)
admin.site.register(StatusCondition)
admin.site.register(Move)
admin.site.register(Item)
admin.site.register(PlayerInventory)
admin.site.register(Rental)
admin.site.register(Profile)

# widget!
class RentalAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }
