import React, { useEffect, useState } from 'react'
import Helmet from 'react-helmet'
import { Link, useParams } from 'react-router-dom'
import axios from '../../HelperFunctions/customAxios'
import EditConditions from './Components/EditConditions';


export default function RoomPatreonConditions() {
  const { roomId } = useParams();
  const [showEditable, setShowEditable] = useState(false);
  const [modalData, setModalData] = useState({});

  useEffect( () => {
    async function fetchCampaignData(){
      const resp = await axios.get(`/api/patreon/${roomId}/campaign`);
      console.log(resp.data.content);
      setModalData(resp.data.content);
    };

    fetchCampaignData();
  }, []);

  return (
    <>
      <Helmet>
        <title>Patreon Conditions - MatrixCerberus</title>
      </Helmet>

      <div className="flex flex-col sm:flex-row items-center justify-around w-full h-48 py-5 shadow-lg bg-dark-eye" >
          <div className='flex w-full justify-center'>
              <div className="hidden sm:w-1/4 sm:block"/>
              <div className='sm:w-3/4 relative font-bold text-2xl m-5 px-3 sm:px-0 text-gray-200'>
                  Patreon Conditions
              </div>
          </div>

          <div className='flex w-full items-center justify-center sm:justify-end sm:mr-4'>
              <Link to={`/rooms/${roomId}`} >
                  <button className="block m-3 px-6 py-3 bg-indigo-700 hover:bg-indigo-600 focus:outline-none rounded">
                      <div className="text-sm font-medium leading-none text-white">
                          Back to Room page
                      </div>
                  </button>
              </Link>
          </div>
      </div>

      <div className="w-full px-6 lg:mx-auto lg:w-10/12">
        <div className="w-full my-3 px-4 pt-4 pb-5 overflow-y-auto">
            <div className='my-4 p-2 rounded-md'>
              {showEditable
                ? <EditConditions roomId={roomId} modalData={modalData} setModalData={setModalData} setShowEditable={setShowEditable} />
                : <></>}

                <button
                className="flex justify-start items-center w-full h-10 border-b border-dark-eye text-black"
                onClick={() => setShowEditable(true)}
                >
                    <div className='flex justify-start items-center w-1/2'>
                        <div className='px-4 py-1 mr-2 bg-gray-900 text-white rounded-lg font-medium'>
                            Campaign
                        </div>

                        <div className='mx-2 font-medium'>
                            Testing
                        </div>
                    </div>

                    <div className='flex justify-end w-1/2'>
                        <svg className="w-4 h-4 ml-3 fill-current" viewBox="0 0 20 20"><path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" fillRule="evenodd"></path></svg>
                    </div>
                </button>
            </div>
        </div>
      </div>
    </>
  )
}
