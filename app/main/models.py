from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=221)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"  # bu qoshimcha ozgartish berilganda ishlatiladi yani izminit orniga adminga


class Tag(models.Model):
    title = models.CharField(max_length=221)

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField(max_length=221)

    def __str__(self):
        return self.question


class Answer(models.Model):
    questions = models.ForeignKey(FAQ, on_delete=models.CASCADE)
    answer = models.TextField()

    def __str__(self):
        return f"answer of {self.questions.question}"


class Subscribe(models.Model):
    email = models.EmailField(unique=True, db_index=True) #unique - bitada ikkimarta jonatomasn #db_index - bu index boyicha qidiradi

    def __str__(self):
        return self.email


class Contact(models.Model):
    name = models.CharField(max_length=221)
    email = models.EmailField(max_length=221)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
