import "./App.css"
import axios from "axios"
import { useReducer, useEffect } from "react"
import List from "./Components/List/List"
import ListItem from "./Components/List/ListItem/ListItem"

function App() {
  const initialState = {
    loading: true,
    listItems: null,
  }
  const [state, dispatch] = useReducer((state, action) => {
    switch (action.type) {
      case "setListItems":
        return {
          ...state,
          loading: false,
          listItems: {
            ...action.payload,
          },
        }
      default:
        return state
    }
  }, initialState)

  useEffect(() => {
    axios
      .get("http://localhost:8000/exhibition/")
      .then(response => {
        dispatch({ type: "setListItems", payload: { ...response.data } })
      })
      .catch(err => {
        console.log(err)
      })
  }, [])
  return (
    <div className="App">
      {state.loading ? null : (
        <List>
          {state.listItems.map((item, index) => {
            return <ListItem content={item.title} key={index} />
          })}
        </List>
      )}
    </div>
  )
}

export default App
