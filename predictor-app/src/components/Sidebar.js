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
import { PickersDay } from '@mui/x-date-pickers/PickersDay';
import Button from '@mui/material/Button';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import FunctionsIcon from '@mui/icons-material/Functions';
import dayjs from 'dayjs';
import LinearProgress from '@mui/material/LinearProgress';
import Badge from '@mui/material/Badge';
import { predict } from '../api';

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

const durationMarks = [
  {
    value: 1,
    label: '1h',
  },
  {
    value: 2,
    label: '2h',
  },
  {
    value: 3,
    label: '3h',
  },
  {
    value: 8,
    label: '8h',
  },
];

const Sidebar = () => {

  const [state, setState] = React.useState({
    brown: true,
    white: true,
    green: true,
    predictionRunning: false,
    predictionDone: false,
    selectedDate: dayjs().add(1, 'day'),
  });

  const handleChange = (event) => {
    setState({
      ...state,
      [event.target.name]: event.target.checked,
    });
  };

  const { brown, white, green, selectedDate, predictionRunning, predictionDone } = state;
  const error = [brown, white, green].filter((v) => v).length < 1;

  const highlightedDays = [];
  for (let i = 1; i < 6; i++) {
    highlightedDays.push(dayjs().add(i, 'day').date());
  }

  function AvailableDay(props) {
    const { highlightedDays = [], day, outsideCurrentMonth, ...other } = props;

    const isSelected =
      !props.outsideCurrentMonth && highlightedDays.indexOf(props.day.date()) >= 0;

    return (
      <Badge
        key={props.day.toString()}
        overlap="circular"
        badgeContent={isSelected ? '✅' : undefined}
      >
        <PickersDay {...other} outsideCurrentMonth={outsideCurrentMonth} day={day} />
      </Badge>
    );
  }

  return (
    <div>
      {
        predictionDone ?

          <Grid container spacing={1} padding={3}>
            <Grid item xs={12}>
              <b>Nächste Leerung {selectedDate.format('DD.MM.YYYY')}</b>
              <LocalizationProvider dateAdapter={AdapterDayjs}>
                <DateCalendar defaultValue={dayjs().add(1, 'day')}
                  disablePast={true}

                  onChange={(newValue) => {
                    if (newValue > dayjs().add(5, 'day')) {
                      console.log('too far in the future');
                    }
                    setState({ ...state, selectedDate: newValue });
                  }}

                  slots={{
                    day: AvailableDay,
                  }}

                  slotProps={{
                    day: {
                      highlightedDays,
                    }
                  }}

                />
              </LocalizationProvider>
            </Grid>

            <Grid item xs={12}>
                <b>Informationen zur Leerung</b>
            </Grid>

            <Grid item xs={12}>
                <Button variant="contained" fullWidth endIcon={<ArrowBackIcon />} onClick={handleBack}>
                  Zurück
                </Button>
            </Grid>

          </Grid>

          :

          <Grid container spacing={1} padding={3}>
            <Grid item xs={12}>
              <h3>Nächste Leerungen Vorhersagen</h3>
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
              <b>Dauer der Tour</b>
              <Slider
                aria-label="Always visible"
                defaultValue={6}
                getAriaValueText={percentValueText}
                step={1}
                marks={durationMarks}
                valueLabelDisplay="on"
                max={8}
                min={0}
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

            <Grid justifyContent="flex-end" item xs={12}>

              {predictionRunning ?

                <div>Glas Sammlung wird berechnet...
                  <LinearProgress /></div> :

                <Button variant="contained" fullWidth endIcon={<FunctionsIcon />} onClick={handlePrediction}>
                  Predict
                </Button>}

            </Grid>

            <Grid justifyContent="flex-end" item xs={12}>

              {predictionDone ? <span>Prediction for {selectedDate.format('DD.MM.YYYY')}</span> : null}
            </Grid>
          </Grid>
      }
    </div>
  );

  function handlePrediction() {
    setState({ ...state, predictionRunning: true });

    predict()
      .then((result) => {
        setState({ ...state, predictionRunning: false, predictionDone: true, predictionResult: result });
      })
      .catch((ex) => console.error(ex));
  }

  function handleBack() {
    setState({ ...state, predictionDone: false });
  }

  function percentValueText(value) {
    return `${value}%`;
  }
};

export default Sidebar;