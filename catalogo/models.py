from __future__ import annotations

from django.db import models
from django.utils import timezone


class Autor(models.Model):
    
    
    #Segun la Ia, al definir los objetos que componen la clase, 
    # se definen [tipo de dato]Field, dado que Field se traduce a campo.:
    #la operacion X=models.CharField se puede traducir a  X es campo de "Chars"(referido a memoria)
    
    """
    Representa a un autor/a.
    Requerido: nombre, email único, biografía opcional.
    """

    # TODO: implementar los campos del modelo
    # Ejemplo de campo:
    # nombre = models.CharField(max_length=120)
    #
    # nombre   → CharField (max_length a elección)
    # email    → EmailField (unique=True)
    # biografia → TextField (blank=True para hacerlo opcional)

    nombre =models.CharField(max_length=120)
    email=models.EmailField(unique=True)#indica que este dato no se puede repetir, unique=unico
    biografia=models.TextField(blank=True)#blank=blanco, basicamente indicas que permite texto en blanco(vacio)

    # Opcional: definir __str__ para que sea legible en el admin y en el shell
    # def __str__(self) -> str:
    #     return self.nombre
    
    
    #Para entenderlo debemos considerar que en python no se emplean un toString()
    #simplemente se escirve print([nombre de objeto]) 
    # por ende el metodo "def __str__(self) -> str:" 
    # define que imprime al tratar al objeto como un string,
    #Nota:note que siempre se emplea la sintaxis  "def__[nobre de metodo]__(self)"
    #para definir un comportamiento especial. Ej:
    
    def __str__(self) -> str:
        return self.nombre
    


class Categoria(models.Model):
    """
    Categoría temática de libros.
    Ejemplos: 'fantasía', 'ciencia ficción', 'historia'.
    """

    # TODO: implementar el campo nombre (unique=True)

    nombre=models.CharField(max_length=120, unique=True)

    # def __str__(self) -> str:
    #     return self.nombre
    
    def __str__(self)->str:
        return self.nombre


class Libro(models.Model):
    """
    Libro del catálogo de la biblioteca.
    Tiene relación N:1 con Autor y N:M con Categoria.
    """

    # TODO: implementar los campos:
    # titulo          → CharField
    # isbn            → CharField (unique=True)
    # fecha_publicacion → DateField
    # cantidad_total  → PositiveIntegerField
    # autor           → ForeignKey(Autor, on_delete=models.PROTECT)
    # categorias      → ManyToManyField(Categoria)
    #
    
    titulo = models.CharField(max_length=300)
    isbn = models.CharField(max_length=13, unique=True)
    fecha_publicacion = models.DateField()#Campo de dia
    cantidad_total = models.PositiveIntegerField()
    autor = models.ForeignKey(Autor, on_delete=models.PROTECT)
    #Foreign=Extranjero
    #key=clave
    #ForeignKey se traduce a "clave extranjera",
    # es decir, un campo que referencia a otro modelo (en este caso, Autor).
    categorias = models.ManyToManyField(Categoria)
    #Esto es como la cardinalidad que aprendi en ISW1, basicamente 
    # un libro puede tener varias categorias 
    # y una categoria puede tener varios libros, p
    # or eso se emplea ManyToManyField, que se traduce a "muchos a muchos",
    # es decir, una relacion de muchos a muchos entre Libro y Categoria.
    
    # Preguntas guía:
    # ¿Qué pasa si eliminás un autor que tiene libros? (PROTECT vs CASCADE)
    # ¿Por qué isbn debe ser único?

    #Es importante definir que ocurre al intentar eliminar un obj
    #on_delete="en eliminacion"
    #model.PROTECT: impide eliminar el objeto que es referenciado por otro objeto.
    #model.CASCADE: elimina en cascada, es decir, elimina el objeto
    # y todos los objetos que lo referencian.
    
    
    #ISBN = International Standard Book Number 
    #(Número Estándar Internacional de Libros)
    #Es un código único que identifica cada libro a nivel mundial(una clave UNICA)
    
    
    
    
    def prestamos_activos(self) -> int:
        """
        Retorna la cantidad de préstamos activos (fecha_devolucion IS NULL).

        Un préstamo es "activo" cuando no se ha registrado devolución.
        """
        # TODO: implementar con ORM usando filter sobre los préstamos relacionados
        # Pista: self.prestamo_set.filter(fecha_devolucion__isnull=True).count()
        #        (o el related_name que hayas definido en Prestamo.libro)
        
        
        # Django "lee" la convención y crea métodos automáticos,
        #es decir que en funcion de como llame a los objetos,
        #Django crea metodos personalizados automaticamente,
        #de esta forma se creo el metodo "prestamo_set"
        

        return self.prestamo_set.filter(fecha_devolucion__isnull=True).count()
    
    

    def disponibles(self) -> int:
        """
        Retorna cuántas copias están disponibles:
        cantidad_total - prestamos_activos()
        """
        # TODO: implementar
        
        return self.cantidad_total - self.prestamos_activos()

    def tiene_disponibles(self) -> bool:
        """Retorna True si hay al menos una copia disponible."""
        # TODO: implementar
        
        return (self.disponibles() > 0)


class Prestamo(models.Model):
    """
    Registro de un préstamo de libro a un usuario.
    Si fecha_devolucion es NULL → el préstamo está activo.
    """

    # TODO: implementar los campos:
    # libro              → ForeignKey(Libro, on_delete=models.CASCADE)
    # nombre_prestatario → CharField
    # fecha_prestamo     → DateField
    # fecha_devolucion   → DateField (null=True, blank=True)
    #
    # Preguntas guía:
    # ¿Por qué usamos CASCADE aquí y PROTECT en Libro→Autor?
    # ¿Qué valor por defecto tendría sentido para fecha_prestamo?
    # Tip: podés usar default=timezone.now si querés fecha automática,
    #      o dejarlo sin default para que el test lo defina explícitamente.

    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    nombre_prestatario = models.CharField(max_length=100)
    fecha_prestamo = models.DateField(default=timezone.now)
    fecha_devolucion = models.DateField(null=True, blank=True)#puede ser nulo o esta vacio

    #CASCADE se emplea aqui porque si se elimina un libro, se eliminan todos los prestamos relacionados
    #Se usa timexone.now para asignar la fecha actual automaticamnete
    #sin recurir a cargar la fecha evidente manualmente"" 
"" 
