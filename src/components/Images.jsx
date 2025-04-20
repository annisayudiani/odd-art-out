const Images = ( {image, altText, artistName, title, year, code, onImageClick, showAnswer} ) => {

  const handleClick = () => {
    if (!showAnswer) {
      if (code === 'a') {
        const correctCount = Number(localStorage.getItem('correct-count')) || 0;
        localStorage.setItem('correct-count', correctCount + 1);
      } else if (code === 'b') {
        const incorrectCount = Number(localStorage.getItem('incorrect-count')) || 0;
        localStorage.setItem('incorrect-count', incorrectCount + 1);
      }
      onImageClick();
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
          tabIndex={1}
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