async function quickstart() {
  // Imports the Google Cloud client library
  const language = require("@google-cloud/language");

  // Creates a client
  const client = new language.LanguageServiceClient();

  /**
   * TODO(developer): Uncomment the following line to run this code.
   */
  const text = "Your text to analyze, e.g. Hello, world!";

  // Prepares a document, representing the provided text
  const document = {
    content: text,
    type: "PLAIN_TEXT",
  };

  // Need to specify an encodingType to receive word offsets
  const encodingType = "UTF8";

  // Detects the sentiment of the document
  const [syntax] = await client.analyzeSyntax({ document, encodingType });

  console.log("Tokens:");
  syntax.tokens.forEach((part) => {
    console.log(`${part.partOfSpeech.tag}: ${part.text.content}`);
    console.log("Morphology:", part.partOfSpeech);
  });
}

quickstart();
