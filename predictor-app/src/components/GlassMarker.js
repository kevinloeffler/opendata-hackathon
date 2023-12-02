import React, { useState } from 'react';
import { MarkerF, InfoWindowF } from '@react-google-maps/api';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';


const GlassMarker = (props) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  const GlassMarkerContent = () => (
    <div
      style={{
        //border: '1px solid #ccc',
        padding: '10px',
        backgroundColor: isOpen ? '#16A74E42' : 'white',
        cursor: 'pointer',
      }}
      onClick={handleToggle}
    >
      <b>Info {props.title}</b>

      <TableContainer style={{ marginTop: '1em' }} component={Paper}>
        <Table sx={{ minWidth: 200 }} aria-label="simple table">
          <TableBody>
            <TableRow key={1} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
              <TableCell component="th" scope="row">
                latitude
              </TableCell>
              <TableCell align="right">{props.position?.lat}</TableCell>

            </TableRow>

            <TableRow key={2} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
              <TableCell component="th" scope="row">
                longitude
              </TableCell>
              <TableCell align="right">{props.position?.lng}</TableCell>

            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>

      <TableContainer style={{ marginTop: '1em' }} component={Paper}>
        <Table sx={{ minWidth: 200 }} aria-label="simple table">
          <TableBody>
            <TableRow key={1} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
              <TableCell component="th" scope="row">
                prediction (datum)
              </TableCell>
              <TableCell align="right">{props.prediction ? props.prediction : 0}</TableCell>

            </TableRow>

            <TableRow key={2} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
              <TableCell component="th" scope="row">
                fill level
              </TableCell>
              <TableCell align="right">{parseFloat(props.level.toFixed(4)) * 100}%</TableCell>

            </TableRow>

            <TableRow key={3} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
              <TableCell component="th" scope="row">
                glass type
              </TableCell>
              <TableCell align="right">{props.type}</TableCell>

            </TableRow>

            <TableRow key={4} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
              <TableCell component="th" scope="row">
                last emptying
              </TableCell>
              <TableCell align="right">{props.date}</TableCell>

            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );

  return (
    <MarkerF position={props.position} onClick={handleToggle}>
      {props.position && isOpen ?
        <InfoWindowF visible={isOpen}>
          <GlassMarkerContent />
        </InfoWindowF> : null}
    </MarkerF>
  );
};

export default GlassMarker;