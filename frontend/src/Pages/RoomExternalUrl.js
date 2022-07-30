import React, { useEffect, useState } from 'react'
import PropTypes from "prop-types"
import { Link, useParams } from 'react-router-dom'
import axios from '../HelperFunctions/customAxios'
import { toast } from "react-toastify"
import 'react-toastify/dist/ReactToastify.css';
import Helmet from 'react-helmet'

const PermanentUrl = ({ urlCode, handleReplace }) => {
    const fullUrl = `${process.env.REACT_APP_BASE_URL}/i/${urlCode}`;
    return (
        <tr className="h-20 text-sm leading-none text-gray-800 bg-gray-200 border-b border-t border-gray-200">
            <td className="pl-4 cursor-pointer">
                <p className='font-medium'> Permanent</p>
            </td>
            <td className="pl-12 cursor-pointer">
                <p className="font-medium"> {urlCode} </p>
            </td>
            <td className="pl-12">
                <p className="font-medium"> {fullUrl} </p>
            </td>
            <td className="pl-12">
                <div className="flex justify-end">
                    <button className="w-5 h-5 mx-4" title="Copy" onClick={() => {
                        navigator.clipboard.writeText(fullUrl);

                        toast.success("Copied to clipboard!", {
                            position: toast.POSITION.TOP_CENTER,
                            autoClose: 3000,
                            hideProgressBar: true
                        });
                    }} >
                        <img className="w-full h-full" src={require("../assets/img/copy-regular.svg").default} />
                    </button>
                    <button className="w-5 h-5 mx-4" title="Replace" onClick={() => handleReplace(urlCode)} >
                        <img className="w-full h-full" src={require("../assets/img/arrow-rotate-right-solid.svg").default} />
                    </button>
                </div>
            </td>
        </tr>
    )
}

PermanentUrl.propTypes = {
    urlCode: PropTypes.string,
    handleReplace: PropTypes.func
}

const TemporaryUrl = ({ urlCode, handleDelete }) => {
    const fullUrl = `${process.env.REACT_APP_BASE_URL}/i/${urlCode}`;
    return (
        <tr className="h-20 text-sm leading-none text-gray-800 bg-white border-b border-t border-gray-100">
            <td className="pl-4 cursor-pointer">
                <p className='font-medium'> Temporary</p>
            </td>
            <td className="pl-12 cursor-pointer">
                <p className="font-medium"> {urlCode} </p>
            </td>
            <td className="pl-12">
                <p className="font-medium"> {fullUrl} </p>
            </td>
            <td className="pl-12">
                <div className="flex justify-end">
                    <button className="w-5 h-5 mx-4" title="Copy" onClick={() => {
                        navigator.clipboard.writeText(fullUrl);

                        toast.success("Copied to clipboard!", {
                            position: toast.POSITION.TOP_CENTER,
                            autoClose: 3000,
                            hideProgressBar: true
                        });
                    }}>
                        <img className="w-full h-full" src={require("../assets/img/copy-regular.svg").default} />
                    </button>
                    <button className="w-5 h-5 mx-4" title="Delete" onClick={() => handleDelete(urlCode)}>
                        <img className="w-full h-full" src={require("../assets/img/delete-icon.svg").default} />
                    </button>
                </div>
            </td>
        </tr>
    )
}

TemporaryUrl.propTypes = {
    urlCode: PropTypes.string,
    handleDelete: PropTypes.func
}

export default function RoomExternalUrl() {
    const { roomId } = useParams();
    const [permanentUrl, setPermanentUrl] = useState('');
    const [temporaryUrl, setTemporaryUrl] = useState([]);

    useEffect( () => {
        async function fetchData() {
            const resp = await axios.get(`/api/rooms/${roomId}/external-url`);
            const data = resp.data.content;
            setPermanentUrl(data.permanent);
            setTemporaryUrl(data.temporary);
        };
        fetchData();
    }, []);

    async function handleReplace(urlCode) {
        const resp = await axios.post(`/api/rooms/${roomId}/external-url/replace?url_code=${urlCode}`);
        setPermanentUrl(resp.data.url_code);
    };

    async function handleDelete(urlCode) {
        const resp = await axios.post(`/api/rooms/${roomId}/external-url/delete?url_code=${urlCode}`);
        if(resp.status == 400) {
            console.error(resp.data);
            toast.error(`Cannot delete ${urlCode}`);
        }
        setTemporaryUrl(urls => urls.filter( url => {
            return url !== urlCode;
        }))
        toast.success(`Successfully deleted ${urlCode}`);
    };

    async function handleCreateNew(useOnceOnly) {
        const resp = await axios.post(`/api/rooms/${roomId}/external-url/new?use_once_only=${useOnceOnly}`);
        setTemporaryUrl(urls => [...urls, resp.data.urlCode])
    }

  return (
    <>
        <Helmet>
			<title>External URLs - MatrixCerberus</title>
        </Helmet>

        <div className="flex flex-col sm:flex-row items-center justify-around w-full h-48 py-5 shadow-lg bg-dark-eye" >
            <div className='flex w-full justify-center'>
                <div className="hidden sm:w-1/4 sm:block"/>
                <div className='sm:w-3/4 relative font-bold text-2xl m-5 px-3 sm:px-0 text-gray-200'>
                    External Urls
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

        <div className="w-full sm:px-6">
                <div className="bg-gray-200 shadow my-3 px-4 md:px-10 pt-4 md:pt-7 pb-5 overflow-y-auto">
                    <table className="w-full whitespace-nowrap">
                        <thead>
                            <tr className="h-16 w-full text-sm leading-none text-gray-800">
                                <th className="font-normal text-left pl-4">Type</th>
                                <th className="font-normal text-left pl-12">URL code</th>
                                <th className="font-normal text-left pl-12">Full URL</th>
                                <th>
                                    <div className='flex items-center justify-end'>
                                        <button
                                        className="block m-3 px-6 py-3 bg-gray-900 hover:bg-indigo-600 focus:outline-none rounded"
                                        onClick={() => handleCreateNew(true)}
                                        >
                                            <div className="text-sm font-medium leading-none text-white">
                                                New Temporary URL
                                            </div>
                                        </button>
                                    </div>
                                </th>
                            </tr>
                        </thead>
                        <tbody className="w-full">
                            <PermanentUrl urlCode={permanentUrl} handleReplace={handleReplace}/>

                            {temporaryUrl.map( (rowValue) => {
                                return <TemporaryUrl urlCode={rowValue} handleDelete={handleDelete} key={rowValue} />
                            })}
                        </tbody>
                    </table>
                </div>
            </div>
    </>
  )
}
