import React from "react"

import Option from "./Option/Options"

import "./Dropdown.css"

const Select = props => {
  return (
    <div className="Select">
      <select name={props.name} id={props.id}>
        <optgroup className="options">{props.children}</optgroup>
      </select>
    </div>
  )
}

const dropdown = {
  Select,
  Option,
}

export default dropdown
