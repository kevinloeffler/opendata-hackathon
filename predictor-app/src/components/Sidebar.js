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
import { getPath, getSensors } from '../api';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Avatar from '@mui/material/Avatar';
import RoomIcon from '@mui/icons-material/Room';
import RecyclingIcon from '@mui/icons-material/Recycling';
import { useSelector, useDispatch } from "react-redux";
import { setPredictedRoute } from '../redux/predictedRouteSlice';
import { setSensors } from '../redux/sensorSlice';

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
  const dispatch = useDispatch();
  const predictedRoute = useSelector((state) => state.predictedRoute.predictedRoute);
  const sensors = useSelector((state) => state.sensor.sensors);

  const [state, setState] = React.useState({
    brown: true,
    white: true,
    green: true,
    predictionRunning: false,
    predictionDone: false,
    selectedDate: dayjs().add(1, 'day'),
    no_empty_if_below: 40,
    tour_duration: 6,
    predictionResult: {},
  });

  const handleChange = (event) => {
    setState({
      ...state,
      [event.target.name]: event.target.checked,
    });
  };

  const { brown, white, green, selectedDate, predictionRunning, predictionDone, no_empty_if_below, tour_duration } = state;
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

                    const selectedIndex = newValue.diff(dayjs(), 'day');
                    dispatch(setPredictedRoute(state.predictionResult.visited_locations[selectedIndex]));

                    filterSensors(selectedIndex, state.predictionResult.visited_locations);
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

            {selectedDate > dayjs().add(5, 'day') ? <div>Keine Vorhersage möglich</div> :

            <Grid container spacing={1}>
            <Grid item xs={12}>
              <Card>
                <CardContent>
                <b>Informationen zur Leerung</b>
                <Typography>
                  Leerung ab Füllstand: {no_empty_if_below}%<br/>
                  Dauer der Tour: {tour_duration}<br />
                  Glasarten: {[state.white ? 'Weiss': '', state.brown ? 'Braun' : '', state.green ? 'Grün' : ''].filter(Boolean).join(', ')}<br/>
                </Typography>
                
                </CardContent>
              </Card>
            </Grid>

            {state.predictionResult ?
            <Grid item xs={12}>
              <Card style={{ backgroundColor: '#16A74E42' }}>
                <CardContent>
                <b>Vorhersage zur Leerung am {selectedDate.format('DD.MM.YYYY')}</b>
                <Typography>
                  Geleerte Glascontainer: {state.predictionResult ? state.predictionResult?.visited_locations[selectedDate.diff(dayjs(), 'day')].length -2 : ''}<br/>
                  Sum. geleerte Kapazitäten: {state.predictionResult ? state.predictionResult?.needed_capacities[selectedDate.diff(dayjs(), 'day')] : ''}<br/>
                  Berechnte Tourdauer (in h): {state.predictionResult ? state.predictionResult?.needed_times[selectedDate.diff(dayjs(), 'day')] / 3600 : ''}h<br/>
                </Typography>
                
                </CardContent>
              </Card>
            </Grid> : null}

            {predictedRoute !== undefined ?
            
            <Grid item xs={12}>
              <b>Tour</b>
              <List sx={{ width: '100%', bgcolor: 'background.paper' }}>

                {predictedRoute.map((sensor, index) => {
                  if (Array.isArray(sensor)) {
                    return (
                      <ListItem key={index}>
                      <ListItemAvatar>
                        <Avatar>
                          <RecyclingIcon />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText primary="KHK St. Gallen" secondary="Sammelstelle" />
                    </ListItem>
                    );
                  }
                  return (
                    <ListItem key={index}>
                      <ListItemAvatar>
                        <Avatar>
                          <RoomIcon />
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText primary={index + ". " + sensor.sensor_id + " (" + sensor.type + ")"} 
                                    secondary={` Erwarteter Füllstand: ` + (parseFloat(sensor.level).toFixed(4) * 100) + "%"} />
                    </ListItem>
                  );
                })}

              </List>

            </Grid>
            : null}

            <Grid item xs={12}>
              <Button variant="contained" fullWidth endIcon={<ArrowBackIcon />} onClick={handleBack}>
                Zurück
              </Button>
            </Grid>

          </Grid> }

          </Grid>

          :

          <Grid container spacing={1} padding={3}>
            <Grid item xs={12}>
              <h3>Nächste Leerungen Vorhersagen</h3>
              <b>Leeren ab Füllstand</b>
              <Slider
                value={no_empty_if_below}
                onChange={(e) => setState({ ...state, no_empty_if_below: e.target.value })}
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
                value={tour_duration}
                onChange={(e) => setState({ ...state, tour_duration: e.target.value })}
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

    const params = {
      brown: state.brown,
      white: state.white,
      green: state.green,
      no_empty_if_below: state.no_empty_if_below,
      tour_duration: state.tour_duration,
    };

    getPath(params)
      .then((result) => {
        dispatch(setPredictedRoute(result.visited_locations[0]));
        setState({ ...state, predictionRunning: false, predictionDone: true, predictionResult: result });
        
        filterSensors(0, result.visited_locations);
      })
      .catch((ex) => console.error(ex));
  }

  function handleBack() {
    dispatch(setPredictedRoute([]));
    setState({ ...state, predictionDone: false, predictionResult: {} });

    fetchSensors();
  }

  function fetchSensors() {
    getSensors()
                .then((result) => {
                  dispatch(setSensors(result));
                })
                .catch((ex) => console.error(ex));
  }

  function percentValueText(value) {
    return `${value}%`;
  }

  function filterSensors(selectedIndex, visited_locations) {
    getSensors()
      .then((result) => {

        const filteredSensors = [];

        for (const sensor of result) {
          for (let i = 1; i < visited_locations[selectedIndex].length - 1; i++) {
            if (sensor.sensor_id.includes(visited_locations[selectedIndex][i].sensor_id)) {
              filteredSensors.push(sensor);
            }
          }
        }
    
        dispatch(setSensors(filteredSensors));
      
      })
      .catch((ex) => console.error(ex));
  }
};

export default Sidebar;