from django.db import models

class Recipe(models.Model):
    """
    A Recipe, links to all the other important bits that make up a recipe
    Uses a custom intermedary model to handle collecting info that is also
    need to reconstruct a full ingredent line.
    """
    #max_length is required.
    title = models.CharField(max_length=20)
    #the attr name needs to be differet than the through tablename.
    #This is case insensitive and has a crappy error message.
    ingredients = models.ManyToManyField('Ingredient', through='IngredientsMap')
    directions = models.TextField()
    notes = models.TextField()
    servings = models.PositiveIntegerField()
    prep_time = models.CharField(max_length=100)
    cooking_time = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title
    
class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self,):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=20)
    abbrev = models.CharField(max_length=20, null=True, blank=True)
    #smaller_unit = models.ManyToManyField('Unit', null=True, blank=True)
    #smaller_scale = models.FloatField(null=True, blank=True)
    #bigger_unit = models.ManyToManyField('Unit', null=True, blank=True)
    #bigger_scale = models.FloatField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name

class IngredientsMap(models.Model):
    ingredient = models.ForeignKey('Ingredient')
    recipie = models.ForeignKey('Recipe')
    amount = models.FloatField()
    unit = models.ForeignKey('Unit')
    notes = models.CharField(max_length=20)

    def __unicode__(self,):
        return "%s in %s" % (self.ingredient,self.recipie)

