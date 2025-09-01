import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from .serializers import ImageUploadSerializer
from PIL import Image
import io

MODEL_PATH = os.path.join(settings.BASE_DIR, 'model_api', 'model', 'best_model.keras')

try:
    print("Memuat model TensorFlow...")
    MODEL = load_model(MODEL_PATH)
    print("Model berhasil dimuat.")
except Exception as e:
    print(f"Gagal memuat model: {e}")
    MODEL = None

# Nama-nama kelas sesuai dengan urutan yang digunakan saat pelatihan
# Pastikan urutan ini sama dengan train_ds.class_names
CLASS_NAMES = ['Rusip', 'belacan', 'bong li piang', 'kretek', 'lakso', 'lempah kuning', 'martabak bangka', 'mie koba', 'otak-otak', 'sambelingkung']
IMAGE_SIZE = (224, 224)

class ModelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # ... (bagian validasi serializer)
        serializer = ImageUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Ambil file gambar dari request
        image_file = serializer.validated_data['image']
        
        try:
            # Baca konten file yang diunggah ke dalam memori
            # Gunakan io.BytesIO untuk membuat objek file-like dari konten
            image_content = image_file.read()
            img_io = io.BytesIO(image_content)
            
            # Sekarang, lewati objek io.BytesIO ke load_img
            img = image.load_img(img_io, target_size=IMAGE_SIZE)
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            
            # Normalisasi gambar sesuai dengan ResNet
            img_array = img_array

            # Lakukan prediksi
            predictions = MODEL.predict(img_array)
            predicted_class_index = np.argmax(predictions[0])
            confidence = float(np.max(predictions[0]))
            print(predicted_class_index)
            
            predicted_class_name = CLASS_NAMES[predicted_class_index]

            response_data = {
                "prediction": predicted_class_name,
                "confidence": confidence,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)