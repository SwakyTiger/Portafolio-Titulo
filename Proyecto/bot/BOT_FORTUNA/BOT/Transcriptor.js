import fs from 'fs';
import Groq from 'groq-sdk';

// Crear una instancia de Groq pasando la clave de API directamente
const groq = new Groq({
  apiKey: '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',
});

// Función para transcribir un archivo de audio
async function transcribirAudio(rutaArchivo) {
  try {
    const transcription = await groq.audio.transcriptions.create({
      file: fs.createReadStream(rutaArchivo), // Leer el archivo de audio
      model: 'whisper-large-v3', // Modelo de transcripción
      prompt: 'Especifica contexto o nombres', // Opcional
      response_format: 'json', // Opcional
      language: 'es', // Idioma (opcional, aquí español)
      temperature: 0.0, // Precisión controlada
    });
    console.log(transcription.text); // Imprimir el texto transcrito
    return transcription.text; // Retornar la transcripción
  } catch (error) {
    console.error('Error al transcribir el archivo:', error);
  }
}

// Llamada de ejemplo a la función, pasando el archivo de audio
transcribirAudio('\prueba2.mp3');
