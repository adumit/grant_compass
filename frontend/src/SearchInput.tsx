
export interface SearchInputProps {
  query?: string;
  handleClick: Function;
}

export default function SearchInput({ query, handleClick}: SearchInputProps) {
  const keyDownHandler = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.code === "Enter") {
      handleClick();
    }
  };

  return (
    <div>
      <input style={{width:250}} id="searchInput" defaultValue={query} onKeyDown={keyDownHandler}/>
      <button className="default-button" style={{marginLeft:1}} onClick={() => {handleClick()}}>
        Search  
      </button>
    </div>
  )
}
