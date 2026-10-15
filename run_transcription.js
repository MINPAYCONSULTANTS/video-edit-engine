const fs = require('fs');
const https = require('https');

const apiKey = process.env.GROQ_API_KEY || '';
if (!apiKey) {
  console.error("GROQ_API_KEY environment variable is required.");
  process.exit(1);
}
const filePath = process.env.AUDIO_FILE || '/Users/sanskarsaraf/.gemini/antigravity/scratch/video_edit/audio.mp3';

const boundary = '----WebKitFormBoundary' + Math.random().toString(16).slice(2);
const fileData = fs.readFileSync(filePath);

let payload = [];
payload.push(Buffer.from('--' + boundary + '\r\n' +
  'Content-Disposition: form-data; name="model"\r\n\r\n' +
  'whisper-large-v3\r\n'));

payload.push(Buffer.from('--' + boundary + '\r\n' +
  'Content-Disposition: form-data; name="response_format"\r\n\r\n' +
  'verbose_json\r\n'));

payload.push(Buffer.from('--' + boundary + '\r\n' +
  'Content-Disposition: form-data; name="timestamp_granularities[]"\r\n\r\n' +
  'segment\r\n'));

payload.push(Buffer.from('--' + boundary + '\r\n' +
  'Content-Disposition: form-data; name="timestamp_granularities[]"\r\n\r\n' +
  'word\r\n'));

payload.push(Buffer.from('--' + boundary + '\r\n' +
  'Content-Disposition: form-data; name="file"; filename="audio.mp3"\r\n' +
  'Content-Type: audio/mpeg\r\n\r\n'));

payload.push(fileData);
payload.push(Buffer.from('\r\n--' + boundary + '--\r\n'));

const fullBody = Buffer.concat(payload);

const req = https.request({
  hostname: 'api.groq.com',
  path: '/openai/v1/audio/transcriptions',
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + apiKey,
    'Content-Type': 'multipart/form-data; boundary=' + boundary,
    'Content-Length': fullBody.length
  }
}, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    console.log('Status:', res.statusCode);
    if (res.statusCode === 200) {
      fs.writeFileSync('/Users/sanskarsaraf/.gemini/antigravity/scratch/video_edit/transcription_full.json', data);
      const parsed = JSON.parse(data);
      console.log('Full text:', parsed.text);
      if (parsed.segments) {
        console.log('Segments count:', parsed.segments.length);
        parsed.segments.forEach(s => console.log(`[${s.start.toFixed(2)}s - ${s.end.toFixed(2)}s]: ${s.text}`));
      }
    } else {
      console.log('Response:', data);
    }
  });
});

req.on('error', e => console.error(e));
req.write(fullBody);
req.end();
