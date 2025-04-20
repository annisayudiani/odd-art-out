import { useState, useEffect } from 'react'
import './App.css'
import Images from './components/Images'
import paintings from './components/util/painting_urls.json'
import Count from './components/Count'

function App() {

  /**
   * Pick n random elements from an array
   * Source: https://labex.io/tutorials/javascript-n-random-elements-in-array-28503
   * @param {[]} [...arr] - An array
   * @param {number} [n] - An optional number to determine the number of element(s) in the output. The default value is 1.
   * @returns {[]} - n random element(s) of the array
   *
   * @example
   *
   *    pickRandomItems([a, b, c, d], 3)
   */
  const pickRandomItems = ([...arr], n = 1) => {
    let m = arr.length;
    while (m) {
      const i = Math.floor(Math.random() * m--);
      [arr[m], arr[i]] = [arr[i], arr[m]];
    }
    return arr.slice(0, n);
  };

  /**
   * Shuffle elements of an array in-place
   * Source: https://dev.to/codebubb/how-to-shuffle-an-array-in-javascript-2ikj
   * @param {[]} - An array
   * @returns {[]} - None
   *
   * @example
   *
   *    shuffleArray([a, b, c, d])
   */
  const shuffleArray = (array) => {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const temp = array[i];
      array[i] = array[j];
      array[j] = temp;
    }
  }

  const [urls, setUrls] = useState([]);
  const [correctArtist, setCorrectArtist] = useState('');
  const [altTexts, setAltTexts] = useState([]);
  const [images, setImages] = useState([]);
  const [artistNames, setArtistNames] = useState([]);
  const [titles, setTitles] = useState([]);
  const [years, setYears] = useState([]);
  const [codes, setCodes] = useState([]);
  const [showAnswer, setShowAnswer] = useState(false);

  const getRandomUrls = () => {
    // Hide the answers and the button
    setShowAnswer(false);

    // Pick two random artists from paintings
    // Assign the first artist as the correctArtist, the second as the incorrectArtist
    const randomArtists = pickRandomItems(Object.keys(paintings), 2);
    const correctArtist = randomArtists[0];
    const incorrectArtist = randomArtists[1];

    // Pick one random painting url from correctArtist
    // Pick three random painting urls from incorrectArtist
    const correctUrl = pickRandomItems(paintings[correctArtist]);
    const incorrectUrls = pickRandomItems(paintings[incorrectArtist], 3);

    // Combine urls into an array
    // Shuffle the array to randomize the order of paintings
    const combinedUrls = [...correctUrl, ...incorrectUrls];
    shuffleArray(combinedUrls);

    // Set the correctArtist for the current round
    // This will be used to determine the correct answer
    setCorrectArtist(correctArtist);

    // Set urls for the current round
    setUrls(combinedUrls);
  }

  const fetchImages = () => {

    // Empty the variables from the previous round
    setImages([]);
    setAltTexts([]);
    setArtistNames([]);
    setTitles([]);
    setYears([]);
    setCodes([]);

    urls.forEach((url) => {
      fetch(url)
        .then((response) => response.json())
        .then((json) => {
          // Fetch painting images
          setImages((prevImages) => [...prevImages, json.primaryImageSmall]);

          // Fetch artist names of each painting
          setArtistNames((prevArtistNames) => [...prevArtistNames, json.artistDisplayName]);

          // Fetch painting titles
          setTitles((prevTitles) => [...prevTitles, json.title]);

          // Fetch painting years
          setYears((prevYears) => [...prevYears, json.objectEndDate]);

          // Fetch painting information for alt texts
          const tags = json.tags.map((tag) => ` ${tag.term}`);
          setAltTexts((prevAltTexts) => [
            ...prevAltTexts,
            `Title: ${json.title}. Medium: ${json.medium}. Contains:${tags}.`,
          ]);

          // Assign code: a is for the correct answer, b is for the incorrect answers
          setCodes((prevCodes) => [...prevCodes,
            json.artistDisplayName === correctArtist ? 'a' : 'b']);
        });
    });
  };

  // Show the answers after players click an image
  const handleImageClick = () => {
    setShowAnswer(true);
  };

  // Get random artists and urls on page load
  useEffect(() => {
    getRandomUrls();
  }, []);

  // Fetch images on page load only after urls are set
  useEffect(() => {
    fetchImages();
  }, [urls]);

  return (
    <>
      <h1>Odd Art Out</h1>
      <div className='subtitle'>
        <p>Three of these paintings were created by the same artist, one by another artist.</p>
        <p><b>Guess the odd one out.</b></p>
        <Count/>
      </div>
      <button
        className={showAnswer ? "active" : "hidden"}
        onClick={getRandomUrls}
        tabIndex={0}
        >
        Next Round
      </button>
      <div className='paintings'>
        {urls.map((url, index) => (
          <Images
            key={index}
            image={images[index]}
            altText={altTexts[index]}
            artistName={artistNames[index]}
            title={titles[index]}
            year={years[index]}
            code={codes[index]}
            onImageClick={handleImageClick}
            showAnswer={showAnswer}
          />
        ))}
      </div>
    </>
  )
}

export default App
