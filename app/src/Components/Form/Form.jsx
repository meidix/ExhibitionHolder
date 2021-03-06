import { useReducer, useEffect } from "react"
import { withFormik, useFormikContext } from "formik"
import axios from "axios"
import * as Yup from "yup"
import Input from "../Input/Input/Input"
import Button from "../Button/Button"
import { MultiSelect } from "react-multi-select-component"
import Loader from "react-loader-spinner"

import "react-loader-spinner/dist/loader/css/react-spinner-loader.css"
import "./Form.css"

const Form = props => {
  const [state, dispatch] = useReducer(
    (state, action) => {
      switch (action.type) {
        case "setCoops":
          return {
            ...state,
            coops: [...action.payload],
          }
        case "setProducts":
          return {
            ...state,
            products: [...action.payload],
          }
        case "loaded":
          return {
            ...state,
            loading: false,
          }
        case "setCoopRequest":
          props.values.coop_request = [...action.payload]
          return {
            ...state,
            values: {
              ...state.values,
              coop_request: [...action.payload],
            },
          }
        case "setProductRequest":
          props.values.product_request = [...action.payload]
          return {
            ...state,
            values: {
              ...state.values,
              product_request: [...action.payload],
            },
          }
        default:
          return {
            ...state,
          }
      }
    },
    {
      loading: true,
      coops: null,
      products: null,
      values: {
        coop_request: [],
        product_request: [],
      },
    }
  )

  useEffect(() => {
    axios
      .get("http://localhost:8000/options/coops/")
      .then(response => {
        dispatch({ type: "setCoops", payload: [...response.data] })
      })
      .catch(err => {
        console.log(err)
      })
  }, [])

  useEffect(() => {
    axios
      .get("http://localhost:8000/options/products/")
      .then(response => {
        dispatch({ type: "setProducts", payload: [...response.data] })
      })
      .catch(err => {
        console.log(err)
      })
  }, [])

  useEffect(() => {
    if (state.coops && state.products) {
      dispatch({ type: "loaded" })
    }
  }, [state.coops, state.products])

  const { isSubmitting } = useFormikContext()

  const handleMultiSelectChange = (e, name) => {
    dispatch({ type: `set${name}`, payload: [...e] })
  }

  return (
    <div>
      <div className="FormWelcome">
        <p>{props.exhibition.form_header}</p>
      </div>
      <form className="Form" onSubmit={props.handleSubmit}>
        <div className="FormGroup">
          <Input
            label="??????"
            type="text"
            name="first_name"
            value={props.values.first_name}
            placeholder="??????"
            changed={props.handleChange}
            validationError={
              props.touched.first_name ? props.errors.first_name : null
            }
            blured={props.handleBlur}
          />
          <Input
            label="?????? ????????????????"
            type="text"
            placeholder="?????? ????????????????"
            name="last_name"
            value={props.values.last_name}
            changed={props.handleChange}
            validationError={
              props.touched.last_name ? props.errors.last_name : null
            }
            blured={props.handleBlur}
          />
          <Input
            label="?????????? ??????????"
            type="text"
            name="cellphone_number"
            value={props.values.cellphone_number}
            changed={props.handleChange}
            validationError={
              props.touched.cellphone_number
                ? props.errors.cellphone_number
                : null
            }
            blured={props.handleBlur}
          />
          <Input
            label="?????????? ????????"
            type="text"
            name="phone_number"
            value={props.values.phone_number}
            changed={props.handleChange}
            validationError={
              props.touched.phone_number ? props.errors.phone_number : null
            }
            blured={props.handleBlur}
          />
        </div>
        <div className="FormGroup">
          <Input
            label="??????/??????????"
            type="text"
            name="state"
            value={props.values.state}
            changed={props.handleChange}
            validationError={props.touched.state ? props.errors.state : null}
            blured={props.handleBlur}
          />
          <Input
            label="?????? ??????"
            type="text"
            name="workplace"
            value={props.values.workplace}
            changed={props.handleChange}
            validationError={
              props.touched.workplace ? props.errors.workplace : null
            }
            blured={props.handleBlur}
          />
          <Input
            label="?????? ????????"
            type="text"
            name="work_position"
            value={props.values.work_position}
            changed={props.handleChange}
            validationError={
              props.touched.work_position ? props.errors.work_position : null
            }
            blured={props.handleBlur}
          />
          <Input
            label="????????"
            type="text"
            name="expertise"
            value={props.values.expertise}
            changed={props.handleChange}
            validationError={
              props.touched.expertise ? props.errors.expertise : null
            }
            blured={props.handleBlur}
          />
        </div>
        <div className="FormGroup">
          <Input
            label="?????? ????????????????????"
            type="email"
            name="email"
            value={props.values.email}
            changed={props.handleChange}
            validationError={props.touched.email ? props.errors.email : null}
            blured={props.handleBlur}
          />
        </div>
        {state.loading ? null : (
          <div className="FormGroup">
            <div className="MultiSelect">
              <label htmlFor="coop_request" className="Label">
                ?????????????? ????????????
              </label>
              <MultiSelect
                options={state.coops}
                className="MultiSelect"
                name="coop_request"
                value={props.values.coop_request}
                onChange={e => handleMultiSelectChange(e, "CoopRequest")}
              />
            </div>
            <div className="MultiSelect">
              <label htmlFor="product_request" className="Label">
                ?????????????? ???????? ????????
              </label>
              <MultiSelect
                options={state.products}
                className="MultiSelect"
                name="product_request"
                value={props.values.product_request}
                onChange={e => handleMultiSelectChange(e, "ProductRequest")}
              />
            </div>
          </div>
        )}
        <div className="FormSubmit">
          <Button type="submit">
            {isSubmitting ? (
              <Loader type="ThreeDots" color="#fff" height={30} width={60} />
            ) : (
              <span className="SubmitButtonLabel">?????????? ??????</span>
            )}
          </Button>
        </div>
      </form>
    </div>
  )
}

export default withFormik({
  mapPropsToValues: () => ({
    first_name: "",
    last_name: "",
    cellphone_number: "",
    phone_number: "",
    expertise: "",
    state: "",
    workplace: "",
    work_position: "",
    email: "",
    coop_request: [],
    product_request: [],
  }),
  validationSchema: Yup.object().shape({
    first_name: Yup.string().max(20).required(),
    last_name: Yup.string().max(30).required(),
    cellphone_number: Yup.string()
      .min(10)
      .max(11)
      .matches(/^(\+98|0)?9[0-9]{9}$/)
      .required(),
    phone_number: Yup.string()
      .min(11)
      .max(11)
      .matches(/^0[1-9]{2}[0-9]{8}$/),
    email: Yup.string().email(),
  }),
  handleSubmit: (values, formikBag) => {
    const data = {
      ...values,
      exhibition: formikBag.props.exhibition.id,
    }
    axios
      .post(
        `http://localhost:8000/visitor/${formikBag.props.exhibition.id}/`,
        data
      )
      .then(response => {
        alert("?????? ?????? ?????? ????")
        formikBag.setSubmitting(false)
        formikBag.resetForm()
      })
      .catch(err => {
        alert(err)
      })
  },
  validateOnBlur: true,
})(Form)
