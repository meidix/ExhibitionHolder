import React from "react"

import "./Input.css"

const Input = props => {
  const classes = ["Input"]
  if (props.validationError) {
    classes.push("Error")
  }
  return (
    <div className="InputGroup">
      {props.label ? (
        <label htmlFor={props.name} className="Label">
          {props.label}
        </label>
      ) : null}
      <input
        type={props.type}
        name={props.name}
        value={props.value}
        onChange={props.changed}
        onBlur={props.blured}
        className={classes.join(" ")}
        placeholder={props.placeholder}
      />
      {props.validationError ? (
        <span className="Error">{props.validationError}</span>
      ) : null}
    </div>
  )
}

export default Input
