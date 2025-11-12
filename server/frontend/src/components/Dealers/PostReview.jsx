import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';

const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  const params = useParams();
  const id = params.id;
  const dealer_url = `/djangoapp/dealer/${id}`;
  const review_url = `/djangoapp/add_review`;
  const carmodels_url = `/djangoapp/get_cars`;

  const postreview = async () => {
    let name = sessionStorage.getItem("firstname") + " " + sessionStorage.getItem("lastname");
    
    // If first and last name are null, use username
    if (name.includes("null")) {
      name = sessionStorage.getItem("username");
    }
    
    if (!model || review === "" || date === "" || year === "" || model === "") {
      alert("All details are mandatory");
      return;
    }

    let model_split = model.split(" ");
    let make_chosen = model_split[0];
    let model_chosen = model_split[1];

    let jsoninput = JSON.stringify({
      "name": name,
      "dealership": parseInt(id),
      "review": review,
      "purchase": true,
      "purchase_date": date,
      "car_make": make_chosen,
      "car_model": model_chosen,
      "car_year": parseInt(year),
    });

    console.log('Submitting review:', jsoninput);
    
    try {
      const res = await fetch(review_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: jsoninput,
      });

      const json = await res.json();
      console.log('Response:', json);
      
      if (json.status === 200) {
        alert("Review posted successfully!");
        window.location.href = `/dealer/${id}`;
      } else {
        alert(`Error: ${json.message || 'Failed to post review'}`);
      }
    } catch (error) {
      console.error('Error posting review:', error);
      alert('Error posting review. Please try again.');
    }
  }

  const get_dealer = async () => {
    const res = await fetch(dealer_url, {
      method: "GET"
    });
    const retobj = await res.json();
    
    if (retobj.status === "success") {  // ✅ CORRETO
      setDealer(retobj.dealer);
    }
  }

  const get_cars = async () => {
    const res = await fetch(carmodels_url, {
      method: "GET"
    });
    const retobj = await res.json();
    
    if (retobj.CarModels) {
      setCarmodels(retobj.CarModels);
    }
  }

  useEffect(() => {
    get_dealer();
    get_cars();
  }, []);

  return (
    <div>
      <Header />
      <div style={{ margin: "5%" }}>
        <h1 style={{ color: "darkblue" }}>{dealer.full_name}</h1>
        <textarea 
          id='review' 
          cols='50' 
          rows='7' 
          placeholder="Write your review here..."
          onChange={(e) => setReview(e.target.value)}
        ></textarea>
        
        <div className='input_field'>
          Purchase Date <input type="date" onChange={(e) => setDate(e.target.value)} />
        </div>
        
        <div className='input_field'>
          Car Make and Model
          <select 
            name="cars" 
            id="cars" 
            onChange={(e) => setModel(e.target.value)}
            defaultValue=""
          >
            <option value="" disabled>Choose Car Make and Model</option>
            {carmodels.map((carmodel, index) => (
              <option 
                key={index} 
                value={carmodel.CarMake + " " + carmodel.CarModel}
              >
                {carmodel.CarMake} {carmodel.CarModel}
              </option>
            ))}
          </select>
        </div>

        <div className='input_field'>
          Car Year 
          <input 
            type="number" 
            onChange={(e) => setYear(e.target.value)} 
            max={2023} 
            min={2015}
            placeholder="2015-2023"
          />
        </div>

        <div>
          <button className='postreview' onClick={postreview}>
            Post Review
          </button>
        </div>
      </div>
    </div>
  )
}

export default PostReview;
