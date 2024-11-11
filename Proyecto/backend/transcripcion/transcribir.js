import fs from 'fs';
import Groq from 'groq-sdk';

const groq = new Groq({
    apiKey: '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',
});

// Función para transcribir un archivo de audio
async function transcribirAudio(rutaArchivo) {
    try {
        const transcription = await groq.audio.transcriptions.create({
            file: fs.createReadStream(rutaArchivo),
            model: 'whisper-large-v3',
            prompt: 'Especifica contexto o nombres',
            response_format: 'json',
            language: 'es',
            temperature: 0.0,
        });
        return transcription.text; // Retornar la transcripción
    } catch (error) {
        console.error('Error al transcribir el archivo:', error);
        process.exit(1); // Salir con un código de error
    }
}

// Obtener la ruta del archivo desde los argumentos de línea de comandos
const rutaArchivo = process.argv[2]; // El segundo argumento es la ruta del archivo
if (rutaArchivo) {
    transcribirAudio(rutaArchivo).then(transcripcion => {
        if (transcripcion) {
            console.log(transcripcion); // Imprimir la transcripción en stdout
        }
    });
} else {
    console.error("No se proporcionó una ruta de archivo.");
    process.exit(1); // Salir con un código de error
}