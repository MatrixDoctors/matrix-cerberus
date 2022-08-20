import axios from '../HelperFunctions/customAxios';
import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types'
import { toast } from 'react-toastify';

export default function PatreonEditConditions({roomId, modalData, setModalData, setRoomConditions, showPatreonEditable, setShowPatreonEditable}) {
    const [currentData, setCurrentData] = useState({});
    const [inputField, setInputField] = useState(0);

    function handleTierCheckboxChange(e){
        const key = e.target.name;
        setCurrentData((previousData) => {
            return {...previousData, tiers: {
                ...previousData.tiers,
                [key]: {
                    ...previousData.tiers[key],
                    is_enabled: !previousData.tiers[key].is_enabled
                }
            }};
        });
    }

    function handleEnableCheckboxChange(e){
        const key = e.target.name;
        setCurrentData((previousData) => {
            return {...previousData, enable_lifetime_support_cents: !previousData.enable_lifetime_support_cents};
        });
    }

    function handleClose(){
        setCurrentData(modalData.data ? {...modalData.data} : {});
        if(modalData.data){
            setInputField("lifetime_support_cents" in modalData.data ? modalData.data.lifetime_support_cents : 0);
        }
        setShowPatreonEditable(false);
    }

    function handleSave(){

        async function saveData(roomId, updatedData){
            const {id, ...dataToBeSent} = updatedData
            const url = `/api/patreon/${roomId}/campaign/${id}`;

            axios.put(url, dataToBeSent)
            .then( () => {
                setModalData(previousData => ({...previousData, data: updatedData}));

                setRoomConditions(previousData => {
                    return previousData.map(item => {
                        if (item.key === modalData.key) {
                            return {...modalData, data: updatedData};
                        }
                        else {
                            return item;
                        }
                    });
                });
                toast.success("Succesfully updated!");
            })
            .catch( () => {
                toast.error("Failed to save data");
            });
        };

        const updatedData = {
            ...currentData,
            lifetime_support_cents: inputField
        };

        saveData(roomId, updatedData);
        handleClose();
    }

    useEffect( () => {
        setCurrentData(modalData.data ? {...modalData.data} : {});
        if(modalData.data){
            setInputField("lifetime_support_cents" in modalData.data ? modalData.data.lifetime_support_cents : 0);
        }
    }, [modalData]);

    return (
    <>
        {showPatreonEditable ? (
            <>
            <div
                className="justify-center items-center flex overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none"
            >
                <div className="relative w-auto my-6 mx-auto max-w-md">
                {/*content*/}
                <div className="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
                    {/*header*/}
                    <div className="flex items-start justify-between py-4 px-6 border-b border-solid border-slate-200 rounded-t">

                        <div className="flex items-center mr-6">
                            <div className="mr-2 w-4 h-4">
                                <img className="w-full h-full" src={require("../assets/img/patreon.svg").default} />
                            </div>

                            <h3 className="text-xl font-semibold">
                                {modalData.thirdPartyAccount} - {modalData.conditionType}
                            </h3>
                        </div>

                        <button
                            className="p-1 ml-auto"
                            onClick={handleClose}
                        >
                            <svg
                            className="w-6 h-6"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg">
                                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                            </svg>
                        </button>
                    </div>

                    {/*body*/}
                    <div className="relative p-6 flex-auto">
                        <div className='mb-4 pb-4 border-b border-solid border-slate-200 rounded-t'>
                        <div className='flex justify-start'>
                                <p className="text-md font-medium text-black">
                                    Owner:
                                </p>
                                <p className="ml-auto pl-4 text-md font-normal text-black">
                                    {modalData.owner.parent}
                                </p>
                            </div>
                            <div className='flex justify-start'>
                                <p className="text-md font-medium text-black">
                                    Campaign name:
                                </p>
                                <p className="ml-auto pl-4 text-md font-normal text-black">
                                    {modalData.data.name}
                                </p>
                            </div>
                        </div>

                        <p className="text-md font-bold text-black">
                            Tiers
                        </p>

                        <div className='p-2 w-full mb-4 pb-4 border-b border-solid border-slate-200 rounded-t'>
                            { "tiers" in currentData
                                ? Object.entries(currentData.tiers).map( ([key, value]) => {
                                    return (
                                        <div key={key}>
                                            <input
                                            className='mr-2'
                                            type="checkbox"
                                            id={`checkbox-${key}`}
                                            name={key}
                                            checked={value.is_enabled}
                                            onChange={(e) => handleTierCheckboxChange(e)}
                                            />
                                            <label htmlFor={`checkbox-${key}`}>{value.title}</label>
                                        </div>
                                    )
                                })
                                : <></>
                            }
                        </div>

                        <p className="text-md font-bold text-black">
                            Life time support cents
                        </p>

                        { "lifetime_support_cents" in currentData
                            ? <div className='p-2 w-full'>
                                <div className='flex items-center'>
                                    <input
                                    className='mr-2'
                                    type="checkbox"
                                    id="enable_lifetime_support_cents"
                                    checked={currentData.enable_lifetime_support_cents}
                                    onChange={handleEnableCheckboxChange}
                                    />
                                    <label htmlFor="enable_lifetime_support_cents">Enabled</label>
                                </div>
                                <div className='flex items-center'>
                                    <label
                                    className="inline-block text-md text-black"
                                    htmlFor="lifetime_support_cents"
                                    >
                                        Total amount:
                                    </label>

                                    <input
                                    type="number"
                                    className='mx-2 p-0.5 bg-gray-100 rounded-md border border-gray-600 focus:ring-blue-500 focus:border-blue-500'
                                    id="lifetime_support_cents"
                                    disabled={!currentData.enable_lifetime_support_cents}
                                    value={inputField}
                                    onChange={(e) => setInputField(e.target.value)}
                                    />
                                </div>
                            </div>
                        : <></>
                        }


                        <div className='flex justify-end items-center mt-3'>
                            <button
                            className="text-white bg-blue-700 hover:bg-blue-800 focus:outline-none font-medium rounded-lg text-sm px-4 py-2 text-center mr-2"
                            onClick={handleSave}
                            >
                                Save
                            </button>

                            <button
                            className="text-white bg-red-700 hover:bg-red-800 focus:outline-none font-medium rounded-lg text-sm px-4 py-2 text-center "
                            onClick={handleClose}
                            >
                                Cancel
                            </button>
                        </div>

                    </div>
                </div>
                </div>
            </div>
            <div className="opacity-25 fixed inset-0 z-40 bg-black"></div>
            </>
        ) : null}
    </>
  )
}

PatreonEditConditions.propTypes = {
    roomId: PropTypes.string,
    modalData: PropTypes.object,
    setModalData: PropTypes.func,
    roomConditions: PropTypes.array,
    setRoomConditions: PropTypes.func,
    showPatreonEditable: PropTypes.bool,
    setShowPatreonEditable: PropTypes.func
}
