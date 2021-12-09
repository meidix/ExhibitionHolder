import "./App.css"
import axios from "axios"
import { useReducer, useEffect } from "react"
import List from "./Components/List/List"
import ListItem from "./Components/List/ListItem/ListItem"

function App() {
  const initialState = {
    loading: true,
    listItems: null,
    current: null,
  }

  const [state, dispatch] = useReducer((state, action) => {
    const setActiveExhibition = data => {
      if (data.length === 1) {
        return data[0].id
      } else {
        return null
      }
    }
    switch (action.type) {
      case "setListItems":
        console.log(action.payload)
        return {
          ...state,
          loading: false,
          listItems: [...action.payload],
          current: setActiveExhibition(action.payload),
        }
      default:
        return state
    }
  }, initialState)

  useEffect(() => {
    axios
      .get("http://localhost:8000/exhibition/")
      .then(response => {
        dispatch({ type: "setListItems", payload: [...response.data] })
      })
      .catch(err => {
        console.log(err)
      })
  }, [])

  const form = null

  return (
    <div className="App">
      {state.loading ? null : state.current ? (
        form
      ) : (
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
