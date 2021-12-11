import React from "react"

import "./Modal.css"

const Modal = ({ width, header, children }) => {
  return (
    <div className="ModalPane">
      <div className="Modal" styles={{ width: width }}>
        <div className="ModalHeader">
          <div className="Title">{header}</div>
          <div className="HeaderDivider"></div>
        </div>
        {children}
      </div>
    </div>
  )
}

export default Modal
