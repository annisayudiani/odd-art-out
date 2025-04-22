/**
 * Count component to display the number of correct and incorrect guesses.
 * It retrieves and updates the counts from localStorage.
 * @returns {JSX.Element} - A component displaying the counts.
 */
const Count = () => {

  // Retrieves the counts from localStorage.
  const correctGuessCount = Number(localStorage.getItem('correct-count')) || 0;
  const incorrectGuessCount = Number(localStorage.getItem('incorrect-count')) || 0;

  return (
    <>
      <p className="count correct">
        {correctGuessCount > 1 ? 'Correct Guesses' : 'Correct Guess'}: {correctGuessCount}
      </p>
      <p className="count incorrect">
        {incorrectGuessCount > 1 ? 'Incorrect Guesses' : 'Incorrect Guess'}: {incorrectGuessCount}
      </p>
    </>
  )
};

export default Count;