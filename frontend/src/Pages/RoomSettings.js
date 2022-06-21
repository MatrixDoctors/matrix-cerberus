import React from 'react'
import PropTypes from "prop-types"

const TableHeader = ({ values }) => {
  return (
    <tr>
      {values.map( (col) => {
        return (
          <th scope="col" className="text-md font-medium text-gray-900 px-6 py-4 text-left" key={col}>
            {col}
          </th>
        )
      })}
    </tr>
  )
}

TableHeader.propTypes = {
  values: PropTypes.arrayOf(PropTypes.string)
}

const TableRows =  ({ values }) => {
  return (
    <>
      {values.map( (row) => {
        return (
          // key is used to uniquely identify a child item
          <tr className="border-b transition duration-300 ease-in-out hover:bg-gray-200" key={row.roomId}>
            <td className="px-6 py-4 whitespace-nowrap text-md font-medium text-gray-900">
              {row.id}
            </td>
            <td className="text-md text-gray-900 font-light px-6 py-4 whitespace-nowrap">
              {row.roomAlias}
            </td>
            <td className="text-md text-gray-900 font-light px-6 py-4 whitespace-nowrap">
              {row.roomId}
            </td>
          </tr>
        )
      })}
    </>
  )
};

TableRows.propTypes = {
  values: PropTypes.arrayOf(PropTypes.object)
}

/**
 * This page lists out all the rooms for which the user is an admin.
 * (Under the assumption that the bot account is also an admin for the same)
 */
export default function RoomSettings() {

  // Dummy data for tables
  const roomHeaderData = ['#', 'Room Alias', 'Room ID'];
  const roomBodyData = [
    {id: 1, roomAlias: "Matrix Cerberus", roomId: "!hMaAAyWsrBAMXEfXso:cadair.com"},
    {id: 2, roomAlias: "GSoC Interns & Mentors 2022", roomId: "!auFsXYPeEIXfseVOEm:ergaster.org"},
    {id: 3, roomAlias: "Element Web/Desktop", roomId: "!YTvKGNlinIzlkMTVRl:matrix.org"}
  ];

  return (
    <div>
			<div className="flex items-center w-full h-48 py-5 shadow-lg bg-dark-eye" >
				<div className='flex items-center justify-center w-full sm:w-1/3'>
					<div className='relative bottom-5 font-bold text-3xl my-5 px-3 sm:px-0 text-gray-200'>
						Room Settings
					</div>
				</div>
				<div className='hidden sm:w-2/3 sm:block'/>
			</div>
			<div className="container mx-auto h-full">
				<div className="flex content-center items-center justify-center h-full ">
					<div className='lg:w-1/12 bg-gray-900' />

					<div className="w-full lg:w-10/12 px-4 ">
						<div className="relative bottom-10 rounded-t mb-0 px-6 py-6 bg-gray-100">

							{/* Account Information */}
							<h6 className="block mb-6 text-gray-800 font-bold">
								Rooms List
							</h6>

              <div className="flex flex-col">
                <div className="overflow-x-auto sm:-mx-6 lg:-mx-8">
                  <div className="py-2 inline-block min-w-full sm:px-6 lg:px-8">
                    <div className="overflow-hidden">
                      <table className="min-w-full">
                        <thead className="bg-gray-300 border-b">
                          <TableHeader values={roomHeaderData} />
                        </thead>
                        <tbody>
                          <TableRows values={roomBodyData} />
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>

						</div>
					</div>

					<div className='lg:w-1/12 bg-gray-900' />
				</div>
			</div>
		</div>
  )
}
