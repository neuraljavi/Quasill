# Importamos las bibliotecas necesarias
import torch
from torch import nn


# Creamos la clase TransformerClassifier que hereda de nn.Module
class TransformerClassifier(nn.Module):
    # Constructor de la clase
    def __init__(self, d_model, num_heads, d_ff, num_layers, input_dim, n_classes, max_length, droput):
        super(TransformerClassifier, self).__init__()

        # Creamos una capa de incrustación (embedding) para convertir los índices de entrada en vectores
        self.embedding = nn.Embedding(input_dim, d_model)

        # Creamos una capa de incrustación (embedding) para codificar las posiciones de las palabras
        self.position_encoding = nn.Embedding(max_length, d_model)

        # Definimos una capa de codificación (encoder) del transformador
        self.encoder_layer = nn.TransformerEncoderLayer(d_model, num_heads, d_ff, droput)

        # Creamos el codificador (encoder) del transformador usando la capa de codificación
        self.encoder = nn.TransformerEncoder(self.encoder_layer, num_layers)

        # Definimos una capa completamente conectada (Fully Connected) para la clasificación final
        self.fc = nn.Linear(d_model, n_classes)

        # Creamos una capa de dropout para evitar el sobreajuste (overfitting)
        self.dropout = nn.Dropout(droput)

    # Método forward que define cómo se realiza la propagación hacia adelante en la red
    def forward(self, x):
        # Creamos una matriz de posiciones para agregar la información posicional a los embeddings
        positions = torch.arange(0, x.size(1)).unsqueeze(0).repeat(x.size(0), 1).to(x.device)

        # Sumamos la incrustación (embedding) de entrada y la codificación de posición, y aplicamos dropout
        x = self.dropout(self.embedding(x) + self.position_encoding(positions))

        # Pasamos la entrada a través del codificador (encoder) del transformer
        x = self.encoder(x)

        # Calculamos la media de las representaciones de las palabras a lo largo de la dimensión temporal (dim=1).
        # La dimensión temporal es la dimensión que contiene las palabras o tokens en la secuencia de entrada.
        # Al obtener la media, estamos creando una única representación fija para toda la secuencia de entrada,
        # que es necesaria para la capa completamente conectada (Fully Connected) que espera un tamaño de entrada fijo.
        x = x.mean(dim=1)

        # Pasamos la representación de las secuencias a través de la capa completamente conectada (Fully Connected)
        x = self.fc(x)

        # Devolvemos el resultado final
        return x
