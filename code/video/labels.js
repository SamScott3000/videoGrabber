async function quickstart() {
  // Imports the Google Cloud Video Intelligence library
  const video = require("@google-cloud/video-intelligence").v1;

  // Creates a client
  const client = new video.VideoIntelligenceServiceClient();

  /**
   * TODO(developer): Uncomment the following line before running the sample.
   */
  const videoName = "Tower1"
  const videoFormat = ".mp4"


  const gcsUri = `gs://sentiment-classification-test/video/${videoName}${videoFormat}`;

  const LabelDetection = {
    labelDetectionMode: ["SHOT_AND_FRAME_MODE"],
    stationaryCamera: false,
    model: "builtin/stable",
    frameConfidenceThreshold: 0.4,
    videoConfidenceThreshold: 0.3
  }

  const videoConfig = {
    labelDetectionConfig: LabelDetection
  }  

  const request = {
    inputUri: gcsUri,
    features: ["LABEL_DETECTION"],
    videoContext: videoConfig,
    outputUri: `gs://sentiment-classification-test/video/${videoName}.txt`,
  };

  // Detects labels in a video
  const [operation] = await client.annotateVideo(request);
  console.log("Waiting for operation to complete...");
  const [operationResult] = await operation.promise();

  // Gets annotations for video
  const annotations = operationResult.annotationResults[0];

  // Write to File
 // var fs = require("fs");

 // var logFile = fs.createWriteStream("output/labelOutput.txt", {
 //   flags: "a",
 //   encoding: "utf-8",
 //   mode: 0744,
 // });


  /* const labels = annotations.segmentLabelAnnotations;
  labels.forEach((label) => {
    console.log(`Label ${label.entity.description} occurs at:`);
    label.segments.forEach((segment) => {
      const time = segment.segment;
      if (time.startTimeOffset.seconds === undefined) {
        time.startTimeOffset.seconds = 0;
      }
      if (time.startTimeOffset.nanos === undefined) {
        time.startTimeOffset.nanos = 0;
      }
      if (time.endTimeOffset.seconds === undefined) {
        time.endTimeOffset.seconds = 0;
      }
      if (time.endTimeOffset.nanos === undefined) {
        time.endTimeOffset.nanos = 0;
      }
      console.log(
        `\tStart: ${time.startTimeOffset.seconds}` +
          `.${(time.startTimeOffset.nanos / 1e6).toFixed(0)}s`
      );
    
      console.log(
        `\tEnd: ${time.endTimeOffset.seconds}.` +
          `${(time.endTimeOffset.nanos / 1e6).toFixed(0)}s`
      );
      
      console.log(`\tConfidence: ${segment.confidence}`);
    });
  });
  */
}

quickstart();
