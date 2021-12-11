import React from "react"

import "./Button.css"

const Button = props => {
  return (
    <button type={props.type} className="Btn" onClick={props.clicked}>
      {props.children}
    </button>
  )
}

export default Button
