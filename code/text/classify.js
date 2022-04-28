async function quickstart() {
// Imports the Google Cloud client library
const language = require('@google-cloud/language');

// Creates a client
const client = new language.LanguageServiceClient();

/**
 * TODO(developer): Uncomment the following lines to run this code
 */
for (let i = 1; i < 82; i++) {

console.log(i)

const bucketName = 'sentiment-classification-test/outputSmall';
const fileName = `${i}.txt`;

// Prepares a document, representing a text file in Cloud Storage
const document = {
  gcsContentUri: `gs://${bucketName}/${fileName}`,
  type: 'PLAIN_TEXT',
};

// Classifies text in the document
const [classification] = await client.classifyText({document});

console.log('Categories:');
classification.categories.forEach(category => {
  console.log(`Name: ${category.name}, Confidence: ${category.confidence}`);
});
}
}

quickstart();
