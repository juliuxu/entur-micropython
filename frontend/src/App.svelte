<script>
  import {
    Label,
    Button,
    Col,
    Row,
    Input,
    Form,
    FormText,
    FormGroup
  } from "sveltestrap";
  const config = {
    wifi_essid: "<essid>",
    wifi_password: "<passord>",
    toggle_delay: 3000,
    quay_id: "NSR:Quay:10851",
    departure_threshold: 120
  };
  async function onSubmit(event) {
    alert("onSubmit");
  }
</script>

<style>
  main {
    padding: 1em;
  }
</style>

<main>
  <Row>
    <Col>
      <h1>MicroEntur</h1>
    </Col>
  </Row>
  <Row>
    <Col>
      <Form on:submit|preventDefault={onSubmit}>
        <FormGroup>
          <Label for="wifi-essid">Wifi Name</Label>
          <Input type="text" id="wifi-essid" bind:value={config.wifi_essid} />
          <FormText color="muted">The name of the your wifi network</FormText>

        </FormGroup>
        <FormGroup>
          <Label for="wifi-password">Wifi Password</Label>
          <Input
            type="text"
            id="wifi-password"
            bind:value={config.wifi_password} />
        </FormGroup>
        <FormGroup>
          <Label for="toggle-delay">Toggle delay (ms)</Label>
          <Input
            type="number"
            id="toggle-delay"
            bind:value={config.toggle_delay} />
          <FormText color="muted">
            The time to wait between showing the current time or next departure
          </FormText>
        </FormGroup>
      </Form>
    </Col>
  </Row>
  <Form>
    <FormGroup>
      <Label for="raw-config">Raw config</Label>
      <Input
        type="textarea"
        name="text"
        id="raw-config"
        value={JSON.stringify(config, 0, 2)} />
    </FormGroup>
    <Button type="submit" color={'primary'}>Save</Button>
  </Form>
  <FormGroup>
    <Button color="danger">Reboot</Button>
  </FormGroup>
</main>
