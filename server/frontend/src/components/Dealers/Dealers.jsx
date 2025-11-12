import React, { useState, useEffect } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png"

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [states, setStates] = useState([]);

  const dealer_url = "/djangoapp/get_dealers/";
  
  const filterDealers = async (state) => {
    if (state === "All") {
      // Se selecionar "All", busca todos novamente
      get_dealers();
      return;
    }
    
    const url = `/djangoapp/get_dealers/${state}`;  // ✅ Cria URL do zero
    
    try {
      const res = await fetch(url, {
        method: "GET"
      });
      const retobj = await res.json();
      
      console.log('Filter response:', retobj);  // Debug
      
      if (retobj.status === "success") {  // ✅ Verifica "success"
        setDealersList(retobj.dealers || []);
      } else {
        console.error('Error filtering dealers:', retobj);
        setDealersList([]);
      }
    } catch (error) {
      console.error('Error:', error);
      setDealersList([]);
    }
  }

  const get_dealers = async () => {
    try {
      const res = await fetch(dealer_url, {
        method: "GET"
      });
      const retobj = await res.json();
      
      console.log('Get dealers response:', retobj);  // Debug
      
      if (retobj.status === "success") {  // ✅ Verifica "success"
        const all_dealers = retobj.dealers || [];
        
        // Extrai estados únicos
        const dealerStates = all_dealers.map(dealer => dealer.state);
        setStates([...new Set(dealerStates)]);
        setDealersList(all_dealers);
      } else {
        console.error('Error getting dealers:', retobj);
        setDealersList([]);
      }
    } catch (error) {
      console.error('Error:', error);
      setDealersList([]);
    }
  }
  
  useEffect(() => {
    get_dealers();
  }, []);

  const isLoggedIn = sessionStorage.getItem("username") != null;
  
  return (
    <div>
      <Header/>
      
      <table className='table'>
        <thead>
          <tr>
            <th>ID</th>
            <th>Dealer Name</th>
            <th>City</th>
            <th>Address</th>
            <th>Zip</th>
            <th>
              <select 
                name="state" 
                id="state" 
                onChange={(e) => filterDealers(e.target.value)}
                defaultValue=""
              >
                <option value="" disabled>State</option>
                <option value="All">All States</option>
                {states.map((state, index) => (
                  <option key={index} value={state}>{state}</option>
                ))}
              </select>
            </th>
            {isLoggedIn && <th>Review Dealer</th>}
          </tr>
        </thead>
        <tbody>
          {dealersList.length > 0 ? (
            dealersList.map(dealer => (
              <tr key={dealer.id}>
                <td>{dealer.id}</td>
                <td>
                  <a href={`/dealer/${dealer.id}`}>{dealer.full_name}</a>
                </td>
                <td>{dealer.city}</td>
                <td>{dealer.address}</td>
                <td>{dealer.zip}</td>
                <td>{dealer.state}</td>
                {isLoggedIn && (
                  <td>
                    <a href={`/postreview/${dealer.id}`}>
                      <img src={review_icon} className="review_icon" alt="Post Review"/>
                    </a>
                  </td>
                )}
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={isLoggedIn ? "7" : "6"}>
                No dealers found
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default Dealers;
