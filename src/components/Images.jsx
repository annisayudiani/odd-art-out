/**
 * Images component to display a painting and its details.
 * Handles click events to reveal the answer and update the game state.
 * @param {Object} props - The props for the component.
 * @param {string} props.image - The URL of the painting image.
 * @param {string} props.altText - The alt text for the image.
 * @param {string} props.artistName - The name of the artist.
 * @param {string} props.title - The title of the painting.
 * @param {number} props.year - The year the painting was created.
 * @param {string} props.code - The code indicating whether the painting is correct ('a') or incorrect ('b').
 * @param {Function} props.onImageClick - The function to call when the image is clicked.
 * @param {boolean} props.showAnswer - Whether to show the answer.
 * @returns {JSX.Element} - A component displaying the painting and its details.
 */
const Images = ( {image, altText, artistName, title, year, code, onImageClick, showAnswer} ) => {

  /**
   * Handle the click event for the image.
   * Updates localStorage only after the first click of each round.
   */
  const handleClick = () => {
    if (!showAnswer) {
      if (code === 'a') {
        const correctCount = Number(localStorage.getItem('correct-count')) || 0;
        localStorage.setItem('correct-count', correctCount + 1);
      } else if (code === 'b') {
        const incorrectCount = Number(localStorage.getItem('incorrect-count')) || 0;
        localStorage.setItem('incorrect-count', incorrectCount + 1);
      }
      onImageClick(); // Call the parent-provided function
    }
  }

  return (
    <>
      <div className={`painting ${showAnswer && `${code}`}`}>
        <img
          src={image}
          alt={altText}
          onClick={handleClick}
          onKeyDown={(e) => {
            if (e.key === "Enter")
                handleClick();
            }}
          tabIndex={0}
        />
        <div className={`description ${showAnswer || `hidden`}`}>
          <h2>Artist: {artistName}</h2>
          <p><b>Title:</b> {title}</p>
          <p><b>Year:</b> {year}</p>
        </div>
      </div>
    </>
  )
}

export default Images;