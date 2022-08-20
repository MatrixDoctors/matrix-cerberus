import React, { useState } from 'react';
import PropTypes from 'prop-types';

export default function GithubPreviewConditions({ modalData, showGithubPreview, setShowGithubPreview }) {
    return (
        <>
        {showGithubPreview ? (
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
                            <div className="mr-2 w-5 h-5">
                                <img className="w-full h-full" src={require("../assets/img/github.svg").default} />
                            </div>

                            <h3 className="text-xl font-semibold">
                                {modalData.thirdPartyAccount} - {modalData.conditionType}
                            </h3>
                        </div>

                        <button
                            className="p-1 ml-auto"
                            onClick={() => setShowGithubPreview(false)}
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
                                <p className="ml-auto text-md font-normal text-black">
                                    {modalData.owner.parent}
                                </p>
                            </div>

                            { modalData.owner.child
                                ? <div className='flex justify-start'>
                                    <p className="text-md font-medium text-black">
                                        Repository:
                                    </p>
                                    <p className="ml-auto text-md font-normal text-black">
                                        {modalData.owner.child}
                                    </p>
                                </div>
                                : <></>
                            }
                        </div>

                        <p className="text-md font-bold text-black">
                            Conditions
                        </p>

                        <div className='p-2 w-full'>
                            { modalData.data
                                ? Object.entries(modalData.data).map( ([key, value]) => {
                                    return (
                                        <div key={key}>
                                            <input
                                            className='mr-2'
                                            type="checkbox"
                                            id={`checkbox-${key}`}
                                            name={key}
                                            disabled={true}
                                            checked={value}
                                            />
                                            <label htmlFor={`checkbox-${key}`}>{key}</label>
                                        </div>
                                    )
                                })
                                : <></>
                            }
                        </div>

                    </div>
                </div>
                </div>
            </div>
            <div className="opacity-25 fixed inset-0 z-40 bg-black"></div>
            </>
        ) : null}
        </>
    );
}

GithubPreviewConditions.propTypes = {
    modalData: PropTypes.object,
    showGithubPreview: PropTypes.bool,
    setShowGithubPreview: PropTypes.func
}
