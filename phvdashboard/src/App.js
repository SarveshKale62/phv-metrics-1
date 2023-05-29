import React,{ useState, useEffect} from 'react';
import './App.css';
import 'react-datepicker/dist/react-datepicker.css';
import pic from'./phvalues logo.jpeg';
import LoadingSpinner from "./LoadingSpinner";
 

function Reactdatepicker()
{
    const [date, setDate]= useState(null);
    // console.log("Date",date)
    const [metrics, setMetrics] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");

    console.log("hi");

    // useEffect(() => {
    //   console.log("hi1");
    //   fetch('/metrics',{
    //   headers : { 
    //     'Content-Type': 'application/json',
    //     'Accept': 'application/json'
    //   }
    //    }).then((response) => 
    //   response.json()).then(data => {
    //     console.log("hi2");
    //     setMetrics(data);
    //     console.log("hi3");
    //   })
    // },[]);
      
    console.log(metrics);
    console.log(metrics[0]);

    const calculateMetrics = (selectedDate) => {
      // console.log("hello");
      setIsLoading(true);
      fetch('/metrics', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ date: selectedDate })
    })
      .then(response => response.json())
      .then(data => {
        setMetrics(data)
        console.log('Metrics calculated:', data);
        setIsLoading(false)
      })
      .catch(error => {
        console.error('Error calculating metrics:', error);
        setErrorMessage("Unable to fetch user list");
        setIsLoading(false);
      });
    };

    const handleDateChange = (event) => {
      const selectedDate = event.target.value;
      setDate(selectedDate);
      calculateMetrics(selectedDate);
    };

    useEffect(() => {
      calculateMetrics(date);
    }, []);

    return( 
       <>
       <div className="Org">
          <img src={pic} alt="logo"></img>
          <h1 className="org_title">PARAM HANSA VALUES</h1>
       </div>
       <div className="Main">
          <div className="Datepicker"> 
          <h1 className="Heading">Selected Date:</h1>
          </div>
          <div className="Datepicker">
          <input type="date" value={date} onChange={handleDateChange} disabled={isLoading} ></input>
          </div>
       </div>
       <div>
          {isLoading ? <LoadingSpinner /> : (
          <>
          {errorMessage && <div className="error">{errorMessage}</div>}
          <table>
            <tr>
              <th>Company Name</th>
              <th>Ticker</th>
              <th>S&P 500 Weight %</th>
              <th>Last Close Price ($)</th>
              <th>Operating Margin %</th>
              <th>EV/(EBITDA-Capex)</th>
              <th>YTD Performance</th>
              <th>Revenue % (1Yr CAGR)</th>
              <th>Net Income % (1Yr CAGR)</th>
              <th>Short interest %</th>
            </tr>
            <tr>
              <td>APPLE</td>
              <td>AAPL</td>
              <td>{metrics[0]?.metrics.sp500_weight}</td>
              <td>{metrics[0]?.metrics.last_close_price}</td>
              <td>{metrics[0]?.metrics.operating_margin}</td>
              <td>{metrics[0]?.metrics.ev_to_ebitda_capex}</td>
              <td>{metrics[0]?.metrics.ytd_performance}</td>
              <td>{metrics[0]?.metrics.revenue_growth}</td>
              <td>{metrics[0]?.metrics.net_income_growth}</td>
              <td>{metrics[0]?.metrics.short_interest}</td>
            </tr>
            <tr>
              <td>AMAZON</td>
              <td>AMZN</td>
              <td>{metrics[1]?.metrics.sp500_weight}</td>
              <td>{metrics[1]?.metrics.last_close_price}</td>
              <td>{metrics[1]?.metrics.operating_margin}</td>
              <td>{metrics[1]?.metrics.ev_to_ebitda_capex}</td>
              <td>{metrics[1]?.metrics.ytd_performance}</td>
              <td>{metrics[1]?.metrics.revenue_growth}</td>
              <td>{metrics[1]?.metrics.net_income_growth}</td>
              <td>{metrics[1]?.metrics.short_interest}</td>
            </tr>
            <tr>
              <td>ALPHABET INC</td>
              <td>GOOGL</td>
              <td>{metrics[2]?.metrics.sp500_weight}</td>
              <td>{metrics[2]?.metrics.last_close_price}</td>
              <td>{metrics[2]?.metrics.operating_margin}</td>
              <td>{metrics[2]?.metrics.ev_to_ebitda_capex}</td>
              <td>{metrics[2]?.metrics.ytd_performance}</td>
              <td>{metrics[2]?.metrics.revenue_growth}</td>
              <td>{metrics[2]?.metrics.net_income_growth}</td>
              <td>{metrics[2]?.metrics.short_interest}</td>
            </tr>
          </table>
          </>
          )}
        </div>
       </> 
    );
}
export default Reactdatepicker;