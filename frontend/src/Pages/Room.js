import React, {useState} from "react";
import { Link, useParams } from "react-router-dom";
import SelectThirdPartyAccountModal from "../Components/SelectThirdPartyAccountModal";

function Room() {
    const { roomId } = useParams();
    const [showModal, setShowModal] = React.useState(false);

    return (
        <>
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
                    <SelectThirdPartyAccountModal showModal={showModal} setShowModal={() => setShowModal()}/>
                </div>

                {/* <div className='hidden sm:w-2/3 sm:block'/> */}
            </div>

            <div className="w-full sm:px-6">
                <div className="bg-gray-200 shadow px-4 md:px-10 pt-4 md:pt-7 pb-5 overflow-y-auto">
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
                            <tr className="h-20 text-sm leading-none text-gray-800 bg-white hover:bg-gray-100 border-b border-t border-gray-100">
                                <td className="pl-4 cursor-pointer">
                                    <div className="flex items-center">
                                        <div className="w-6 h-6">
                                            <img className="w-full h-full" src={require("../assets/img/github.svg").default} />
                                        </div>
                                        <div className="pl-4">
                                            <p className="font-medium">GitHub</p>
                                        </div>
                                    </div>
                                </td>
                                <td className="pl-12 cursor-pointer">
                                    <p className="font-medium"> TestOrgForCerberus </p>
                                    <p className="text-xs leading-3 text-gray-600 mt-2">SampleRepo</p>
                                </td>
                                <td className="pl-12 ">
                                    <p className="text-sm font-medium leading-none text-gray-800"> Repository </p>
                                </td>
                                <td className="pl-12">
                                    <div className="flex justify-end">
                                        <button className="w-5 h-5 mx-4" title="Show">
                                            <img className="w-full h-full" src={require("../assets/img/eye-regular.svg").default} />
                                        </button>
                                        <button className="w-5 h-5 mx-4" title="Edit">
                                            <img className="w-full h-full" src={require("../assets/img/pen-to-square.svg").default} />
                                        </button>
                                        <button className="w-5 h-5 mx-4" title="Delete">
                                            <img className="w-full h-full" src={require("../assets/img/delete-icon.svg").default} />
                                        </button>
                                    </div>
                                </td>
                            </tr>

                            <tr className="h-20 text-sm leading-none text-gray-800 border-b border-t bg-white hover:bg-gray-100 border-gray-100">
                                <td className="pl-4 cursor-pointer">
                                    <div className="flex items-center">
                                        <div className="w-6 h-6">
                                            <img className="w-full h-full" src={require("../assets/img/github.svg").default} />
                                        </div>
                                        <div className="pl-4">
                                            <p className="font-medium">GitHub</p>
                                        </div>
                                    </div>
                                </td>
                                <td className="pl-12 cursor-pointer">
                                    <p className="font-medium"> TestOrgForCerberus </p>
                                </td>
                                <td className="pl-12 ">
                                    <p className="text-sm font-medium leading-none text-gray-800"> Teams</p>
                                </td>
                                <td className="pl-12">
                                    <div className="flex justify-end">
                                        <button className="w-5 h-5 mx-4" title="Show">
                                            <img className="w-full h-full" src={require("../assets/img/eye-regular.svg").default} />
                                        </button>
                                        <button className="w-5 h-5 mx-4" title="Edit">
                                            <img className="w-full h-full" src={require("../assets/img/pen-to-square.svg").default} />
                                        </button>
                                        <button className="w-5 h-5 mx-4" title="Delete">
                                            <img className="w-full h-full" src={require("../assets/img/delete-icon.svg").default} />
                                        </button>
                                    </div>
                                </td>
                            </tr>

                            {/* Row - 3 */}
                            <tr className="h-20 text-sm leading-none text-gray-800 border-b border-t bg-white hover:bg-gray-100 border-gray-100">
                                <td className="pl-4 cursor-pointer">
                                    <div className="flex items-center">
                                        <div className="w-6 h-6">
                                            <img className="w-full h-full" src={require("../assets/img/patreon.svg").default} />
                                        </div>
                                        <div className="pl-4">
                                            <p className="font-medium">Patreon</p>
                                        </div>
                                    </div>
                                </td>
                                <td className="pl-12 cursor-pointer">
                                    <p className="font-medium"> Kuries </p>
                                </td>
                                <td className="pl-12 ">
                                    <p className="text-sm font-medium leading-none text-gray-800"> Sponsorship Tiers </p>
                                </td>
                                <td className="pl-12">
                                    <div className="flex justify-end">
                                        <button className="w-5 h-5 mx-4" title="Show">
                                            <img className="w-full h-full" src={require("../assets/img/eye-regular.svg").default} />
                                        </button>
                                        <button className="w-5 h-5 mx-4" title="Edit">
                                            <img className="w-full h-full" src={require("../assets/img/pen-to-square.svg").default} />
                                        </button>
                                        <button className="w-5 h-5 mx-4" title="Delete">
                                            <img className="w-full h-full" src={require("../assets/img/delete-icon.svg").default} />
                                        </button>
                                    </div>
                                </td>
                            </tr>


                        </tbody>
                    </table>
                </div>
            </div>
        </>
    );
}

export default Room;
