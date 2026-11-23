const fontnik = require('fontnik');
const fs = require('fs');
const path = require('path');

const fontFile = process.argv[2];
const outputDir = process.argv[3] || 'fonts';
const fontName = process.argv[4] || 'Noto Sans Regular';

if (!fontFile) {
  console.error('Usage: node generate-fonts.js <font.ttf> [outputDir] [fontName]');
  process.exit(1);
}

const font = fs.readFileSync(fontFile);
const dir = path.join(outputDir, fontName);
fs.mkdirSync(dir, { recursive: true });

async function generate() {
  for (let start = 0; start < 65536; start += 256) {
    const end = start + 255;
    const data = await new Promise((resolve, reject) => {
      fontnik.range({ font, start, end }, (err, res) => {
        if (err) reject(err);
        else resolve(res);
      });
    });
    fs.writeFileSync(path.join(dir, `${start}-${end}.pbf`), data);
  }
  console.log(`Generated 256 glyph ranges for "${fontName}" in ${dir}`);
}

generate().catch(err => { console.error(err); process.exit(1); });
