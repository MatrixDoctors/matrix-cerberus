import React, {useEffect, useState} from "react";
import Helmet from "react-helmet";
import PropTypes from "prop-types"
import { Link, useParams } from "react-router-dom";
import SelectThirdPartyAccountModal from "../Components/SelectThirdPartyAccountModal";
import GithubPreviewConditions from "../Components/GithubPreviewConditions";
import axios from "../HelperFunctions/customAxios";
import GithubEditConditions from "../Components/GithubEditConditions";
import PatreonPreviewConditions from "../Components/PatreonPreviewConditions";
import PatreonEditConditions from "../Components/PatreonEditConditions";

const Images = {
    'github': require('../assets/img/github.svg').default,
    'patreon': require('../assets/img/patreon.svg').default,
}

const TableRows = ({rowValue, setShowGithubPreview, setShowGithubEditable, setShowPatreonPreview, setShowPatreonEditable, setModalData, handleDelete}) => {
    const owner= rowValue.owner;
    const image = Images[rowValue.thirdPartyAccount.toLowerCase()];

    return (
        <tr className="h-20 text-sm leading-none text-gray-800 bg-white hover:bg-gray-100 border-b border-t border-gray-100">
            <td className="pl-4 cursor-pointer">
                <div className="flex items-center">
                    <div className="w-6 h-6">
                        <img className="w-full h-full" src={image} />
                    </div>
                    <div className="pl-4">
                        <p className="font-medium">{rowValue.thirdPartyAccount}</p>
                    </div>
                </div>
            </td>

            <td className="pl-12 cursor-pointer">
                <p className="font-medium"> {owner.parent} </p>
                { owner.child
                    ? <p className="text-xs leading-3 text-gray-600 mt-2">{owner.child}</p>
                    : <></>}
            </td>

            <td className="pl-12 ">
                <p className="text-sm font-medium leading-none text-gray-800"> {rowValue.conditionType} </p>
            </td>
            <td className="pl-12">
                <div className="flex justify-end">
                    <button
                    className="w-5 h-5 mx-4"
                    title="Show"
                    onClick={() => {
                        setModalData(rowValue);
                        if(rowValue.thirdPartyAccount == 'Github'){
                            setShowGithubPreview(true);
                        }
                        else if(rowValue.thirdPartyAccount == 'Patreon'){
                            setShowPatreonPreview(true);
                        }
                    }}
                    >
                        <img className="w-full h-full" src={require("../assets/img/eye-regular.svg").default} />
                    </button>

                    <button
                    className="w-5 h-5 mx-4"
                    title="Edit"
                    onClick={() => {
                        setModalData(rowValue);
                        if(rowValue.thirdPartyAccount == 'Github'){
                            setShowGithubEditable(true);
                        }
                        else if(rowValue.thirdPartyAccount == 'Patreon'){
                            setShowPatreonEditable(true);
                        }
                    }}
                    >
                        <img className="w-full h-full" src={require("../assets/img/pen-to-square.svg").default} />
                    </button>
                    <button
                    className="w-5 h-5 mx-4"
                    title="Delete"
                    onClick={() => handleDelete(rowValue)}>
                        <img className="w-full h-full" src={require("../assets/img/delete-icon.svg").default} />
                    </button>
                </div>
            </td>
        </tr>
    )
}

TableRows.propTypes = {
    rowValue: PropTypes.object,
    setShowGithubPreview: PropTypes.func,
    setShowGithubEditable: PropTypes.func,
    setShowPatreonPreview: PropTypes.func,
    setShowPatreonEditable: PropTypes.func,
    setModalData: PropTypes.func,
    handleDelete: PropTypes.func
}

function Room() {
    const { roomId } = useParams();
    const [showModal, setShowModal] = useState(false);
    const [roomConditions, setRoomConditions] = useState([]);

    const [showGithubPreview, setShowGithubPreview] = useState(false);
    const [showGithubEditable, setShowGithubEditable] = useState(false);

    const [showPatreonPreview, setShowPatreonPreview] = useState(false);
    const [showPatreonEditable, setShowPatreonEditable] = useState(false);

    const [modalData, setModalData] = useState({});

    function handleDelete(rowData) {
        async function deleteData(roomId, rowData){
            const thirdPartyAccount = rowData.thirdPartyAccount.toLowerCase();
            const conditionType = rowData.conditionType.toLowerCase();
            const ownerType = rowData.type;

            let url;
            if(thirdPartyAccount === 'github') {
                url = `/api/rooms/${roomId}/github/${ownerType}/${conditionType}/delete`;

                // Excludes the 'key' and updates the 'data' property.
                let dataToBeSent = {
                    "type": ownerType,
                    "third_party_account": thirdPartyAccount,
                    "owner": rowData.owner,
                    "condition_type": conditionType,
                    "data": rowData.data
                }

                return axios.post(url, dataToBeSent);
            }
            if(thirdPartyAccount === 'patreon') {
                url = `/api/patreon/${roomId}/campaign/delete?campaign_id=${rowData.data.id}`;
                return axios.post(url);
            }
        }

        deleteData(roomId, rowData)
        .then(() => {
            setRoomConditions(previousData => previousData.filter(item => item.key !== rowData.key) );
        })
        .catch((err) => {
            console.error("Could not delete the room condition ", err);
        });
    }

    useEffect( () => {
        async function fetchRoomConditions() {
            const resp = await axios.get(`/api/rooms/${roomId}`);
            const data = resp.data.map( (item) => {
                let key = item.third_party_account + item.owner.parent + item.condition_type;
                if(item.owner.child) {
                    key += item.owner.child;
                }
                return {
                    type: item.type,
                    thirdPartyAccount: item.third_party_account,
                    owner: item.owner,
                    conditionType: item.condition_type,
                    data: item.data,
                    key: key
                };
            });
            setRoomConditions(data);
        };
        fetchRoomConditions();
    }, [])

    return (
        <>
            <Helmet>
			    <title>Room - MatrixCerberus</title>
            </Helmet>

            <div className="flex flex-col md:flex-row items-center justify-around w-full h-48 py-5 shadow-lg bg-dark-eye" >
                <div className='flex w-full justify-center'>
                    <div className="hidden md:w-1/4 sm:block"/>
                    <div className='md:w-3/4 relative font-bold text-lg md:text-2xl m-5 px-3 sm:px-0 text-gray-200'>
                        { roomId }
                    </div>
                </div>

                <div className='flex w-full items-center justify-center md:justify-end md:mr-4'>
                    <Link to={`/rooms/${roomId}/external-url`} >
                        <button className="block m-3 px-6 py-3 bg-green-600 hover:bg-indigo-600 focus:outline-none rounded">
                            <div className="text-sm font-medium leading-none text-white">
                                External URLs
                            </div>
                        </button>
                    </Link>

                    <button
                    className="block m-3 px-6 py-3 bg-indigo-700 hover:bg-indigo-600 focus:outline-none rounded"
                    onClick={() => setShowModal(true)}
                    >
                        <p className="text-sm font-medium leading-none text-white">Add Condition</p>
                    </button>
                    <SelectThirdPartyAccountModal roomId={roomId} showModal={showModal} setShowModal={() => setShowModal()}/>
                </div>

                {/* <div className='hidden sm:w-2/3 sm:block'/> */}
            </div>

            <div className="w-full sm:px-6">
                <div className="bg-gray-200 shadow px-4 md:px-10 pt-4 md:pt-7 pb-5 overflow-y-auto">
                    <GithubPreviewConditions modalData={modalData} showGithubPreview={showGithubPreview} setShowGithubPreview={setShowGithubPreview} />
                    <GithubEditConditions
                        roomId={roomId}
                        modalData={modalData}
                        setModalData={setModalData}
                        setRoomConditions={setRoomConditions}
                        showGithubEditable={showGithubEditable}
                        setShowGithubEditable={setShowGithubEditable}
                    />

                    <PatreonPreviewConditions modalData={modalData} showPatreonPreview={showPatreonPreview} setShowPatreonPreview={setShowPatreonPreview} />
                    <PatreonEditConditions
                        roomId={roomId}
                        modalData={modalData}
                        setModalData={setModalData}
                        setRoomConditions={setRoomConditions}
                        showPatreonEditable={showPatreonEditable}
                        setShowPatreonEditable={setShowPatreonEditable}
                    />
                    <table className="w-full whitespace-nowrap">
                        <thead>
                            <tr className="h-16 w-full text-sm leading-none text-gray-800">
                                <th className="font-normal text-left pl-4">Third Party Account</th>
                                <th className="font-normal text-left pl-12">Owner</th>
                                <th className="font-normal text-left pl-12">Conditions type</th>
                            </tr>
                        </thead>
                        <tbody className="w-full">
                            {/* Row - 1 */}
                            {roomConditions.map( (rowValue) => {
                                return (
                                    <TableRows
                                        rowValue={rowValue}
                                        key={rowValue.key}
                                        setShowGithubPreview={setShowGithubPreview}
                                        setShowGithubEditable={setShowGithubEditable}
                                        setShowPatreonPreview={setShowPatreonPreview}
                                        setShowPatreonEditable={setShowPatreonEditable}
                                        setModalData={setModalData}
                                        handleDelete={handleDelete}
                                    />
                                )
                            })}

                        </tbody>
                    </table>
                </div>
            </div>
        </>
    );
}

export default Room;
