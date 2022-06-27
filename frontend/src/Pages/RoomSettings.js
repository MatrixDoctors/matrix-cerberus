import React, { useEffect, useState } from 'react'
import PropTypes from "prop-types"
import axios from '../HelperFunctions/customAxios'

const TableHeader = ({ colValue }) => {
  return (
      <th scope="col" className="text-md font-medium text-gray-900 px-6 py-4 text-left">
        {colValue}
      </th>
  )
}

TableHeader.propTypes = {
  colValue: PropTypes.string
}

const TableRows =  ({ rowValue }) => {
  return (
    <tr className="border-b transition duration-300 ease-in-out hover:bg-gray-200">
      <td className="px-6 py-4 whitespace-nowrap text-md font-medium text-gray-900">
        {rowValue.id}
      </td>
      <td className="text-md text-gray-900 font-light px-6 py-4 whitespace-nowrap">
        {rowValue.roomAlias}
      </td>
      <td className="text-md text-gray-900 font-light px-6 py-4 whitespace-nowrap">
        {rowValue.roomId}
      </td>
    </tr>
  )
};

TableRows.propTypes = {
  rowValue: PropTypes.object
}

/**
 * This page lists out all the rooms for which the user is an admin.
 * (Under the assumption that the bot account is also an admin for the same)
 */
export default function RoomSettings() {

  const roomHeaderData = ['#', 'Room Alias', 'Room ID'];
  const [roomBodyData, setRoomBodyData] = useState([]);

  useEffect( () => {
    async function fetchRoomData() {
      const resp = await axios.get('api/users/room-list');
      const data = resp.data.content;

      let roomData = [], index=1;
      for(let key in data){
        roomData.push({
          id: index,
          roomAlias: data[key],
          roomId: key
        })
        index += 1;
      }
      setRoomBodyData(roomData);
    }
    fetchRoomData();
  }, []);

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
                          <tr>
                            {roomHeaderData.map( (colValue) => {
                              return <TableHeader colValue={colValue} key={colValue}/>
                            })}
                          </tr>
                        </thead>
                        <tbody>
                          {roomBodyData.map( (rowValue) => {
                            return <TableRows rowValue={rowValue} key={rowValue.roomId}/>
                          })}
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
