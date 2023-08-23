// Compressor.ts

export class Compressor {
  // LZW Compression
  static lzwEncode(s: string): string {
    const dict: { [key: string]: number } = {};
    let data = (s + "").split("");
    let out = [];
    let currChar;
    let phrase = data[0];
    let code = 256; // Start code (after all single chars)

    for (let i = 1; i < data.length; i++) {
      currChar = data[i];
      if (dict[phrase + currChar] != null) {
        phrase += currChar;
      } else {
        out.push(phrase.length > 1 ? dict[phrase] : phrase.charCodeAt(0));
        dict[phrase + currChar] = code;
        code++;
        phrase = currChar;
      }
    }
    out.push(phrase.length > 1 ? dict[phrase] : phrase.charCodeAt(0));

    // Convert the output values into a string
    return out.map((code) => String.fromCharCode(code)).join("");
  }

  // LZW Decompression
  static lzwDecode(s: string): string {
    const dict: { [key: number]: string } = {};
    let data = (s + "").split("").map((char) => char.charCodeAt(0));
    let currChar = String.fromCharCode(data[0]);
    let oldPhrase = currChar;
    let out = [currChar];
    let code = 256; // Start code (after all single chars)
    let phrase;

    for (let i = 1; i < data.length; i++) {
      let currCode = data[i];
      if (currCode < 256) {
        phrase = String.fromCharCode(data[i]);
      } else {
        phrase = dict[currCode] ? dict[currCode] : oldPhrase + currChar;
      }
      out.push(phrase);

      currChar = phrase.charAt(0);
      dict[code] = oldPhrase + currChar;
      code++;

      oldPhrase = phrase;
    }

    return out.join("");
  }
}
