import * as React from 'react';
import Grid from '@mui/material/Grid';
import FormLabel from '@mui/material/FormLabel';
import FormControl from '@mui/material/FormControl';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormHelperText from '@mui/material/FormHelperText'; import Slider from '@mui/material/Slider';
import Checkbox from '@mui/material/Checkbox';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DateCalendar } from '@mui/x-date-pickers/DateCalendar';
import Button from '@mui/material/Button';
import FunctionsIcon from '@mui/icons-material/Functions';
import dayjs from 'dayjs';
import LinearProgress from '@mui/material/LinearProgress';

const marks = [
  {
    value: 0,
    label: '0%',
  },
  {
    value: 40,
    label: '40%',
  },
  {
    value: 80,
    label: '80%',
  },
  {
    value: 100,
    label: '100%',
  },
];

const Sidebar = () => {

  const [state, setState] = React.useState({
    brown: true,
    white: true,
    green: true,
    predictionRunning: false,
    predictionDone: false,
    selectedDate: dayjs(),
  });

  const handleChange = (event) => {
    setState({
      ...state,
      [event.target.name]: event.target.checked,
    });
  };

  const { brown, white, green, selectedDate, predictionRunning, predictionDone } = state;
  const error = [brown, white, green].filter((v) => v).length < 1;

  return (
    <Grid container spacing={1} padding={3}>
      <Grid item xs={12} sm={6}>
        <b>Nächste Leerung</b>
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <DateCalendar defaultValue={dayjs()} />
        </LocalizationProvider>
      </Grid>

      <Grid item xs={12}>
        <b>Leeren ab Füllstand</b>
        <Slider
          aria-label="Always visible"
          defaultValue={80}
          getAriaValueText={percentValueText}
          step={10}
          marks={marks}
          valueLabelDisplay="on"
        />
      </Grid>

      <Grid item xs={12}>
        <b>Glasarten</b>
        <FormControl
          required
          error={error}
          component="fieldset"
          sx={{ m: 3 }}
          variant="standard"
        >
          <FormLabel component="legend">Glas auswählen</FormLabel>
          <FormGroup>
            <FormControlLabel
              control={
                <Checkbox checked={green} onChange={handleChange} name="green" />
              }
              label="Grün"
            />
            <FormControlLabel
              control={
                <Checkbox checked={brown} onChange={handleChange} name="brown" />
              }
              label="Braun"
            />
            <FormControlLabel
              control={
                <Checkbox checked={white} onChange={handleChange} name="white" />
              }
              label="Weiss"
            />
          </FormGroup>
          <FormHelperText>Bitte mindestens 1 Glasart auswählen</FormHelperText>
        </FormControl>
      </Grid>

      <Grid item xs={12}>
        <FormControlLabel
          control={<Checkbox color="secondary" name="showRoute" value="yes" />}
          label="Route anzeigen"
        />
      </Grid>

      <Grid justifyContent="flex-end" item xs={12}>

        { predictionRunning ? 
        
        <div>Predicting glass collection...
        <LinearProgress /></div> :

        <Button variant="contained" fullWidth endIcon={<FunctionsIcon />} onClick={handlePrediction}>
          Predict
        </Button>}
      
      </Grid>

      <Grid justifyContent="flex-end" item xs={12}>
         
        {predictionDone ? <span>Prediction for {selectedDate.format('DD.MM.YYYY')}</span> : null}
      </Grid>
    </Grid>
  );

  function handlePrediction() {
    setState({ ...state, predictionRunning: true });
  }

  function percentValueText(value) {
    return `${value}%`;
  }
};

export default Sidebar;