import React from 'react'
import PropTypes from 'prop-types'
import { Link } from 'react-router-dom';

export default function SelectThirdPartyAccountModal({ roomId, showModal, setShowModal }) {
  return (
    <>
      {showModal ? (
        <>
          <div
            className="justify-center items-center flex overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none"
          >
            <div className="relative w-auto my-6 mx-auto max-w-sm">
              {/*content*/}
              <div className="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
                {/*header*/}
                <div className="flex items-start justify-between py-4 px-6 border-b border-solid border-slate-200 rounded-t">
                  <h3 className="text-xl font-semibold">
                    Add room conditions
                  </h3>
                  <button
                    className="p-1 ml-auto "
                    onClick={() => setShowModal(false)}
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

                    <p className="text-sm font-normal text-black">
                        Select one of the third party accounts to view available options.
                    </p>

                    <ul className="my-4 space-y-3">
                        <li>
                          <Link to={`/rooms/${roomId}/github-conditions`} >
                            <button className='flex justify-start items-center w-full p-2 border bg-gray-200 hover:bg-gray-300 rounded-md'>
                                <div className="w-4 h-4">
                                    <img className="w-full h-full" src={require("../assets/img/github.svg").default} />
                                </div>
                                <div className="pl-4">
                                    <p className="font-medium">GitHub</p>
                                </div>
                            </button>
                          </Link>
                        </li>
                        <li>
                          <Link to={`/rooms/${roomId}/patreon-conditions`} >
                              <button className='flex justify-start items-center w-full p-2 border bg-gray-200 hover:bg-gray-300 rounded-md'>
                                  <div className="w-4 h-4">
                                      <img className="w-full h-full" src={require("../assets/img/patreon.svg").default} />
                                  </div>
                                  <div className="pl-4">
                                      <p className="font-medium">Patreon</p>
                                  </div>
                              </button>
                          </Link>
                        </li>
                    </ul>

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

SelectThirdPartyAccountModal.propTypes = {
  roomId: PropTypes.string,
  showModal: PropTypes.bool,
  setShowModal: PropTypes.func
}
