async function quickstart() {
  // Imports the Google Cloud client library
  const language = require("@google-cloud/language");

  // Instantiates a client
  const client = new language.LanguageServiceClient();

  // The text to analyze
  const text = "Hello, world, What is up!";

  const document = {
    content: text,
    type: "PLAIN_TEXT",
  };

  // Detects the sentiment of the text
  const [result] = await client.analyzeSentiment({ document: document });
  const sentiment = result.documentSentiment;

  const fs = require('fs');

  fs.writeFile("output/text.txt", `Sentiment score: ${sentiment.score}`, function(err) {
    if(err) {
        return console.log(err);
    }
    console.log("The file was saved!");
}); 

  console.log(`Text: ${text}`);
  console.log(`Sentiment score: ${sentiment.score}`);
  console.log(`Sentiment magnitude: ${sentiment.magnitude}`);
}

quickstart();
