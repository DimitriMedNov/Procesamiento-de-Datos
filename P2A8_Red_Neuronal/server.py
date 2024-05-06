import numpy as np
import logging
import tensorflow as tf
import tensorflow_datasets as tfds
from urllib import parse
from http.server import HTTPServer, BaseHTTPRequestHandler

# Jesus D'mitri Medina Novelo

logger = tf.get_logger()
logger.setLevel(logging.ERROR)

dataset, metadata = tfds.load('mnist', as_supervised=True, with_info=True)
train_dataset, test_dataset = dataset['train'], dataset['test']

class_names = [
    'Cero', 'Uno', 'Dos', 'Tres', 'Cuatro', 'Cinco', 'Seis', 'Siete',
    'Ocho', 'Nueve'
]

num_train_examples = metadata.splits['train'].num_examples  # 60 mil datos train
num_test_examples = metadata.splits['test'].num_examples  # 10 mil datos test


# Normalizar: Numeros de 0 a 255, que sean de 0 a 1
def normalize(images, labels):
    images = tf.cast(images, tf.float32)
    images /= 255
    return images, labels


train_dataset = train_dataset.map(normalize)
test_dataset = test_dataset.map(normalize)

# Estructura de la red
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28, 1)),  # Capa de entrada
    tf.keras.layers.Dense(64, activation=tf.nn.relu),  # Capas oculta
    tf.keras.layers.Dense(64, activation=tf.nn.relu),  # Capas oculta
    tf.keras.layers.Dense(10, activation=tf.nn.softmax)  # para clasificacion
])

# Función que compila el modelo
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Aprendizaje por lotes de 32 cada lote
BATCHSIZE = 32
train_dataset = train_dataset.repeat().shuffle(num_train_examples).batch(BATCHSIZE)
test_dataset = test_dataset.batch(BATCHSIZE)

# Entrenamiento
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print("Peticion recibida")
        #Obtener datos de la petición y limpiar los datos
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        data = data.decode().replace('pixeles=', '')
        data = parse.unquote(data)
        #Realizar transformación para dejar igual que los ejemplos que usa MNIST
        arr = np.fromstring(data, np.float32, sep=",")
        arr = arr.reshape(28,28)
        arr = np.array(arr)
        arr = arr.reshape(1,28,28,1)
        arr = 1 - arr
        arr /= 255.0
        arr = arr.reshape(1, 28, 28, 1)
        #Realizar y obtener la predicción
        prediction_values = model.predict(arr, batch_size=1)
        prediction = str(np.argmax(prediction_values))
        print("Prediccion final: " + prediction)
        # Regresar respuesta a la peticion HTTP
        self.send_response(200)
        # Evitar problemas con CORS
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(prediction.encode())

#Iniciar el servidor en el puerto 8000 y escuchar por siempre
#Si se queda colgado, en el admon de tareas buscar la tarea de python y finalizar tarea
print("Iniciando el servidor...")
server = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
server.serve_forever()


