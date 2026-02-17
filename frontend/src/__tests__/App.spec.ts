import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import App from '../App.vue'
import {
  editerMembre,
  supprimerMembre,
  chargerMembres,
  sauvegarderMembre,
  annuler,
  editMode
} from '../useMembres'

describe('App', () => {
  it('mounts renders properly', () => {
    const wrapper = mount(App)
    expect(wrapper.text()).toContain('You did it!')
  })
})
describe('Formulaires',() =>{
  test('affiche les membres', ()=>{
    const wrapper = mount(editerMembre(membre),{
      props
    })
  })
})
